#!/usr/bin/python

import cgi
import timecard
import sqlite3

print("Content-Type: text/html")
print()

form = cgi.FieldStorage()
if "name" in form:
    db = sqlite3.connect(timecard.timecard_db)
    c = db.cursor()
    c.execute("INSERT INTO users(name) VALUES (?)", (form['name'].value,))
    timecard.printredir()
    db.commit()
    db.close()
else:
    print("Status: 400 Bad Request")
    print()
    print("No name specified")

