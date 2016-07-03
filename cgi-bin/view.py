#!/usr/bin/python

import cgi
import timecard
import sqlite3

print("Content-Type: text/plain")
print()

form = cgi.FieldStorage()
db = sqlite3.connect("timecard.db")
c = db.cursor()
c.execute("SELECT name, uid, logged_in FROM users")
users = c.fetchall()

print("UID\tName\tLogged In")
for k in users:
    print("{}\t{}\t{}".format(k[1], k[0], k[2]))


db.commit()
db.close()

