import sqlite3


db = sqlite3.connect("timecard.db")
c = db.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS sessions
            (uid integer, begin_time text, end_time text)''')
c.execute('''CREATE TABLE IF NOT EXISTS users
            (name text, uid integer PRIMARY KEY, logged_in integer DEFAULT 0, last_login text, type text)''')

db.commit()
db.close()
