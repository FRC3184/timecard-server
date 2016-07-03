#!/usr/bin/python

import sqlite3
import cgi
import hashlib
import http.cookies
import os
import timecard

print("Content-Type: text/html")

db = sqlite3.connect(timecard.timecard_db)
c = db.cursor()

cookie = http.cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
session_id = cookie['session'].value

c.execute("DELETE FROM session WHERE session_id=?", (session_id,))

db.commit()
db.close()

print()
print("If you were logged in before, you aren't now. <a href='login.html'>Login again</a>")
