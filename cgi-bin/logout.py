#!/usr/bin/python

import cgi
import sqlite3
import timecard

print("Content-Type: text/html")

form = cgi.FieldStorage()
if "name" in form:
    db = sqlite3.connect("timecard.db")
    c = db.cursor()

    c.execute("SELECT uid, logged_in FROM users WHERE name=?", (form['name'].value,))
    rows = c.fetchall()
    if len(rows) != 1:
        print("Status: 500 Internal Server Error")
        print()
        print(timecard.err(0, len(rows)))
    else:
        uid = rows[0][0]
        if rows[0][1] == 0:  # User is not logged in
            print()
            print("Can't log out user because user is not logged in!")
        else:
            c.execute("INSERT INTO events(uid, date, event_type) VALUES (?, datetime('now'), 'logout')", (int(uid),))
            c.execute("UPDATE users SET logged_in=0 WHERE uid=?", (uid,))
            print()
            timecard.printredir()
    db.commit()
    db.close()
else:
    print("Status: 400 Bad Request")
    print()
    print("No name specified")
