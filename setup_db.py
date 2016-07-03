import sqlite3


db = sqlite3.connect("timecard.db")
c = db.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS events
            (uid integer, date text, event_type text)''')
c.execute('''CREATE TABLE IF NOT EXISTS users
            (name text, uid integer PRIMARY KEY, logged_in integer DEFAULT 0)''')
c.execute('''CREATE TABLE IF NOT EXISTS users
    (name text, uid integer PRIMARY KEY, logged_in integer DEFAULT 0)''')

c.execute('''INSERT INTO users(name) VALUES ('Chris Tyler')''')
c.execute("INSERT INTO events VALUES (?, datetime('now'), 'login')", [0])

db.commit()
db.close()
