#!/usr/bin/python

import cgi
import timecard
import sqlite3

print("Content-Type: text/html")
print()

print(timecard.html_header.format(title="View Users", css='''
th, table, td {
    border: 1px solid black;
}
'''))

form = cgi.FieldStorage()
db = sqlite3.connect(timecard.timecard_db)
c = db.cursor()
c.execute("SELECT name, uid, logged_in FROM users")
users = c.fetchall()

print("<table>")
print("<tr><th>UID</th><th>Name</th><th>Logged In</th></tr>")
for k in users:
    print("<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(k[1], k[0], "Yes" if k[2] == 1 else "No"))

print("</table>")
print(timecard.html_ending)


db.commit()
db.close()

