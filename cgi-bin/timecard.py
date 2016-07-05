import datetime
import sqlite3
import os
import http.cookies

errorcodes = {
    0: "USER_NOT_FOUND"
}

timeformat = "%Y-%m-%d %H:%M:%S"


timecard_db = "/srv/http/timecard.db"


html_header = '''<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style type="text/css">{css}</style>
</head>
<body>
'''

html_ending = '''</body></html>'''


def err(code, debug_info):
    return "{}:{}:{}".format(code, errorcodes[code], debug_info)


def printredir(location="./action.py"):
    print('''
    <!DOCTYPE html>
    <head>
        <title>Redirect</title>
    </head>
    <body>
        Success. <a href="{0}">Click here if you are not automatically redirected</a>
        <script type="text/javascript">
        window.location = "{0}";
        </script>
    </body>
    </html>
    '''.format(location))


class CentralTime(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours=6) - self.dst(dt)

    def dston(self, year):
        date = datetime.datetime(year=year, month=3, day=1, hour=2)
        days_ahead = 6 - date.weekday()
        if days_ahead < 0:
            days_ahead += 7
        return date + datetime.timedelta(days=(days_ahead+7))  # Add another 7, because second sunday

    def dstoff(self, year):
        date = datetime.datetime(year=year, month=11, day=1, hour=2)
        days_ahead = 6 - date.weekday()
        if days_ahead < 0:
            days_ahead += 7
        return date + datetime.timedelta(days=days_ahead)

    def dst(self, dt):
        if self.dston(dt.year) <= dt.replace(tzinfo=None) < self.dstoff(dt.year):
            return datetime.timedelta(hours=1)
        else:
            return datetime.timedelta(0)

    def tzname(self, dt):
        return "US/Central"


def get_current_timezone():
    return CentralTime()  # Can't be bothered


def verify_auth():
    try:
        cookie = http.cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
        session_id = cookie['session'].value

        db = sqlite3.connect(timecard_db)
        c = db.cursor()
        c.execute("SELECT auth_name, session_begin FROM session WHERE session_id=?", (session_id,))
        rows = c.fetchall()
        if len(rows) != 1:
            return False
        return True  # TODO check for session timeout?
    except (KeyError, http.cookies.CookieError):
        return False  # No session

