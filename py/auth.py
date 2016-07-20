import http.cookies
import timecard
import hashlib
import datetime
import sys

errors = {
    0: "None",
    1: "Incorrect password",
    2: "Could not find user"
}


def login(c, environ):
    """
    Try to login a user
    :param environ: WSGI environment
    :param c: Database cursor
    :return: Status, content, headers
    """

    form = timecard.parse_post(environ)
    try:
        username = form[b'user'][0].decode("utf-8")
        password = form[b'pass'][0].decode("utf-8")
    except KeyError:
        return 400, [], [("Location", "/login.html")]

    c.execute("SELECT pass, salt FROM auth WHERE user=?", (username,))
    rows = c.fetchall()
    if len(rows) == 1:
        hash1 = hashlib.sha256(password.encode('utf-8')).hexdigest()
        hash2 = hashlib.sha256((hash1 + rows[0][1]).encode('utf-8')).hexdigest()  # Salt the hashed password
        if hash2 == rows[0][0]:
            session_id = hashlib.md5(str(datetime.datetime.now())
                                     .encode('utf-8')).hexdigest()  # Set the id to be the hashed time

            c.execute("INSERT INTO session (auth_name, session_id, session_begin) VALUES "
                      "(?, ?, datetime('now', 'localtime'))",
                      (username, session_id))

            return 303, [""], [("Set-Cookie", "session={}; path=/".format(session_id)),
                               timecard.get_location_header("/")]
        else:
            return 401, timecard.html_begin() + ["Bad username/password combination"] + timecard.html_end(), []
    else:
        return 401, timecard.html_begin() + ["Could not find user"] + timecard.html_end(), []


def logout(c, environ):
    """
    Dumb logout.
    :param c: Database cursor
    :param environ: WSGI Environment
    :return: Status, content, headers
    """
    session_id = http.cookies.SimpleCookie(environ["HTTP_COOKIE"]).get("session").value
    c.execute("DELETE FROM session WHERE session_id=?", (session_id,))

    return 303, [], [timecard.get_location_header("/")]


def verify_auth(c, environ):
    """
    Verify that a user is logged in and their login is correct
    :param c: Database cursor
    :param environ: WSGI Environment
    :return: True if the user login (by session cookie) is valid, otherwise false
    """
    try:
        session_id = http.cookies.SimpleCookie(environ["HTTP_COOKIE"]).get("session").value

        c.execute("SELECT auth_name, session_begin FROM session WHERE session_id=?", (session_id,))
        rows = c.fetchall()

        if len(rows) != 1:
            return False
        return True  # TODO check for session timeout?
    except (KeyError, http.cookies.CookieError) as ex:
        return False  # No session
