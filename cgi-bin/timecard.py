import datetime

errorcodes = {
    0: "USER_NOT_FOUND"
}

timeformat = "%Y-%m-%d %H:%M:%S"


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
