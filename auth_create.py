import sqlite3
import hashlib

user = input("What is the username? ")
password = input("What is the password? ")
salt = input("What is the salt? ")

hash1 = hashlib.sha256(password.encode('utf-8')).hexdigest()
hash2 = hashlib.sha256((hash1 + salt).encode('utf-8')).hexdigest()  # Salt the hashed password

db = sqlite3.connect("timecard.db")
c = db.cursor()

c.execute('''INSERT INTO auth(user, pass, salt) VALUES (?, ?, ?)''', (user, hash2, salt))

db.commit()
db.close()
