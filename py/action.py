import auth
import timecard
import barcode
import barcode.writer
import barcode.codex
from io import StringIO, BytesIO

import sys


def login(c, environ):
    form = timecard.get_data(environ)
    plain = "plain" in form

    content = [] if plain else timecard.html_begin()
    status = 200
    headers = []

    if auth.verify_auth(c, environ):
        if b"name" in form:
            username = form[b'name'][0].decode("utf-8")

            c.execute("SELECT uid, logged_in FROM users WHERE UPPER(name)=?", (username.upper(),))
            rows = c.fetchall()
            if len(rows) != 1:
                status = 400
                content += ["User not found: " + username]
            else:
                uid = int(rows[0][0])
                if rows[0][1] == 1:  # User is logged in
                    status = 400
                    content += ["Can't log in user because user is already logged in!"]
                else:
                    c.execute(
                        "INSERT INTO events(uid, date, event_type) VALUES (?, datetime('now', 'localtime'), 'login')",
                        (int(uid),))
                    c.execute("UPDATE users SET logged_in=1 WHERE uid=?", (uid,))
                    # Redirect
                    status = 303
                    headers += [timecard.get_location_header("/")]
        else:
            status = 400
            print("No name specified")
    else:
        status = 401
        if plain:
            content += ["Not logged in/Session not valid"]
        else:
            content += ["<a href='/login.html'>Please login</a>"]
    return status, content + ([] if plain else timecard.html_end()), headers


def logout(c, environ):
    form = timecard.get_data(environ)
    plain = "plain" in form

    content = [] if plain else timecard.html_begin()
    status = 200
    headers = []

    if auth.verify_auth(c, environ):
        if b"name" in form:
            username = form[b'name'][0].decode("utf-8")

            c.execute("SELECT uid, logged_in FROM users WHERE UPPER(name)=?", (username.upper(),))
            rows = c.fetchall()
            if len(rows) != 1:
                status = 400
                content += ["User not found: " + username]
            else:
                uid = int(rows[0][0])
                if rows[0][1] == 0:  # User is not logged in
                    status = 400
                    content += ["Can't log out user because user is not logged in!"]
                else:
                    c.execute(
                        "INSERT INTO events(uid, date, event_type) VALUES (?, datetime('now', 'localtime'), 'logout')",
                        (int(uid),))
                    c.execute("UPDATE users SET logged_in=0 WHERE uid=?", (uid,))
                    # Redirect
                    status = 303
                    headers += [timecard.get_location_header("/")]
        else:
            status = 400
            content += ["No name specified"]
    else:
        status = 401
        if plain:
            content += ["Not logged in/Session not valid"]
        else:
            content += ["<a href='/login.html'>Please login</a>"]
    return status, content + ([] if plain else timecard.html_end()), headers


def create_user(c, environ):
    form = timecard.get_data(environ)

    status = 200
    content = timecard.html_begin()

    if auth.verify_auth(c, environ):
        if "name" in form:
            c.execute("INSERT INTO users(name) VALUES (?)", (form['name'],))
            print()
        else:
            status = 400
            content += ["No name specified"]
    else:
        status = 401
        content += ["<a href='/login.html'>Please login</a>"]
    return status, content + timecard.html_end(), []


def gen_barcode(c, environ):
    form = timecard.get_data(environ)

    content = []
    status = 200
    headers = []

    if b"name" in form:
        username = form[b'name'][0].decode("utf-8")

        data = username  # Change to some UID?

        opts = {"module_height": 8.0, "text_distance": 3.0}

        barcode_writer = barcode.writer.SVGWriter()
        barcode_writer.set_options(opts)
        barc = barcode.codex.Code39(data, barcode_writer, add_checksum=False)
        dummy = BytesIO()
        barc.write(dummy, opts)
        content = [dummy.getvalue().decode()]
        dummy.close()

        headers += [("Content-Type", "image/svg")]
    else:
        status = 400
        content += ["No name specified"]
    return status, content, headers
