#!/usr/bin/python

import sqlite3
import cgi
import hashlib
import http.cookies
import datetime
import timecard

print("Content-Type: text/html")

form = cgi.FieldStorage()
if 'user' in form and 'pass' in form:
    username = form['user'].value
    password = form['pass'].value

    db = sqlite3.connect(timecard.timecard_db)
    c = db.cursor()
    c.execute("SELECT pass, salt FROM auth WHERE user=?", (username,))
    rows = c.fetchall()
    if len(rows) == 1:
        hash1 = hashlib.sha256(password.encode('utf-8')).hexdigest()
        hash2 = hashlib.sha256((password + rows[0][1]).encode('utf-8')).hexdigest()  # Salt the hashed password
        if hash2 == rows[0][0]:
            session_id = hashlib.md5(str(datetime.datetime.now())
                                     .encode('utf-8')).hexdigest()  # Set the id to be the hashed time

            c.execute("INSERT INTO session (auth_name, session_id, session_begin) VALUES (?, ?, datetime('now'))",
                      (username, session_id))

            sessionCookie = http.cookies.SimpleCookie()
            sessionCookie['session'] = session_id
            print(sessionCookie)
            print()
            timecard.printredir("index.html")
        else:
            print()
            print("Incorrect password for user {}".format(username))
    else:
        print()
        print("Could not find user {}".format(username))
    db.commit()
    db.close()
else:
    print()
    print("User and/or pass not in form data")
