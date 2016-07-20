import sqlite3
import hashlib
import datetime

user = input("What is the username? ")
password = input("What is the password? ")
salt = hashlib.sha256(str(datetime.datetime.now())).hexdigest()[0:8]  # 32 bit salt

hash1 = hashlib.sha256(password.encode('utf-8')).hexdigest()
hash2 = hashlib.sha256((hash1 + salt).encode('utf-8')).hexdigest()  # Salt the hashed password

db = sqlite3.connect("timecard.db")
c = db.cursor()

c.execute('''INSERT INTO auth(user, pass, salt) VALUES (?, ?, ?)''', (user, hash2, salt))

db.commit()
db.close()
