#!/usr/bin/python

import cgi
import sqlite3
import timecard

print("Content-Type: text/html")

if timecard.verify_auth():
    form = cgi.FieldStorage()
    if "name" in form:
        db = sqlite3.connect(timecard.timecard_db)
        c = db.cursor()

        c.execute("SELECT uid, logged_in FROM users WHERE name=?", (form['name'].value,))
        rows = c.fetchall()
        if len(rows) != 1:
            print("Status: 500 Internal Server Error")
            print()
            print(timecard.err(0, len(rows)))
        else:
            uid = int(rows[0][0])
            if rows[0][1] == 1:  # User is not logged in
                print()
                print("Can't log in user because user is already logged in!")
            else:
                c.execute("INSERT INTO events(uid, date, event_type) VALUES (?, datetime('now'), 'login')", (int(uid),))
                c.execute("UPDATE users SET logged_in=1 WHERE uid=?", (uid,))
                print()
                timecard.printredir()
        db.commit()
        db.close()
    else:
        print("Status: 400 Bad Request")
        print()
        print("No name specified")
else:
    print("Status: 401 Unauthorized")
    print()
    print("<a href='/login.html'>Please login</a>")