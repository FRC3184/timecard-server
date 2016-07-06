#!/usr/bin/python

import cgi
import sqlite3
import timecard

form = cgi.FieldStorage()
plain = 'plain' in form
print("Content-Type: text/{}".format("plain" if plain else "html"))

if timecard.verify_auth():
    if "name" in form:
        db = sqlite3.connect(timecard.timecard_db)
        c = db.cursor()

        c.execute("SELECT uid, logged_in FROM users WHERE name=?", (form['name'].value,))
        rows = c.fetchall()
        if len(rows) != 1:
            print("Status: 400 Bad Request")
            print()
            print("User not found: " + form['name'].value)
        else:
            uid = rows[0][0]
            if rows[0][1] == 0:  # User is not logged in
                print("Status: 400 Bad Request")
                print()
                print("Can't log out user because user is not logged in!")
            else:
                c.execute(
                    "INSERT INTO events(uid, date, event_type) VALUES (?, datetime('now', 'localtime'), 'logout')",
                    (int(uid),))
                c.execute("UPDATE users SET logged_in=0 WHERE uid=?", (uid,))
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
    if plain:
        print("Not logged in/Session not valid")
    else:
        print("<a href='/login.html'>Please login</a>")
