#!/usr/bin/python

import cgi
import timecard
import sqlite3


class User:
    def __init__(self, uid, name, logged_in):
        self.uid = uid
        self.name = name
        self.logged_in = logged_in

print("Content-Type: text/plain")
print()

form = cgi.FieldStorage()
db = sqlite3.connect(timecard.timecard_db)
c = db.cursor()
c.execute("SELECT name, uid, logged_in FROM users")
users = c.fetchall()

usermap = {}
for k in users:
    usermap[k[1]] = User(k[1], k[0], k[2])

c.execute("SELECT uid, date, event_type FROM events")
events = c.fetchall()

for event in sorted(events, key=lambda x: x[1], reverse=True):
    print("{} {} at {}".format(usermap[event[0]].name, event[2], event[1]))

db.commit()
db.close()
