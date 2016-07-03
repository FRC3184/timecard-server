#!/usr/bin/python

import cgi
import timecard
import sqlite3
import time
import datetime

epoch = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=datetime.timezone.utc)


def unix_time(dt):
    return (dt - epoch).total_seconds()


class User:
    def __init__(self, uid, name, logged_in):
        self.uid = uid
        self.name = name
        self.logged_in = logged_in

print("Content-Type: text/plain")
print()

form = cgi.FieldStorage()
db = sqlite3.connect("timecard.db")
c = db.cursor()
c.execute("SELECT name, uid, logged_in FROM users")
users = c.fetchall()

usermap = {}
for k in users:
    usermap[k[1]] = User(k[1], k[0], k[2])

c.execute("SELECT uid, date, event_type FROM events")
events = c.fetchall()
events = sorted(events, key=lambda x: x[1])

# oh how i hate timezones
print("Name\tTime Spent (hh:mm:ss)")
for uid, user in usermap.items():
    sumtime = 0
    uevents = list(filter(lambda x: x[0] == uid, events))
    if len(uevents) % 2 != 0:
        now = datetime.datetime.now()
        sumtime += int(unix_time(now.replace(tzinfo=datetime.timezone.utc) +
                                 timecard.get_current_timezone().utcoffset(now)) -
                       unix_time(datetime.datetime.strptime(uevents[-1][1], timecard.timeformat)
                                 .replace(tzinfo=datetime.timezone.utc)))
        uevents = uevents[:-1]
    for i in range(0, len(uevents), 2):
        login = uevents[i]
        logout = uevents[i+1]
        timelogin = unix_time(datetime.datetime.strptime(login[1], timecard.timeformat)
                              .replace(tzinfo=datetime.timezone.utc))
        timelogout = unix_time(datetime.datetime.strptime(logout[1], timecard.timeformat)
                               .replace(tzinfo=datetime.timezone.utc))
        sumtime += timelogout - timelogin
    timespent = datetime.timedelta(seconds=sumtime)
    seconds = timespent.total_seconds()
    total_hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds %= 60
    print("{}\t{}:{}:{}".format(user.name, total_hours, minutes, int(seconds)))

db.commit()
db.close()
