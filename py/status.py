import auth
import datetime
import config
import timecard


epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time(dt):
    return (dt - epoch).total_seconds()


class User:
    def __init__(self, uid, name, logged_in):
        self.uid = uid
        self.name = name
        self.logged_in = logged_in


def events(c, environ):
    """
    Generate a page of events
    :param c: Database cursor
    :param environ: WSGI Environment
    :return: Response code, Content, headers
    """
    content = timecard.html_begin()
    status = 200
    if auth.verify_auth(c, environ):

        c.execute("SELECT name, uid, logged_in FROM users")
        users = c.fetchall()

        usermap = {}
        for k in users:
            usermap[k[1]] = User(k[1], k[0], k[2])

        c.execute("SELECT uid, date, event_type FROM events")
        events = c.fetchall()

        for event in sorted(events, key=lambda x: x[1], reverse=True):
            content += ["<span class='event'>{} {} at {}</span><br />"
                        .format(usermap[event[0]].name, event[2], event[1])]

    else:
        status = 401
        content += ["<a href='/login.html'>Please login</a>"]
    return status, content + timecard.html_end(), []


def view(c, environ):

    content = timecard.html_begin()
    status = 200
    if auth.verify_auth(c, environ):

        c.execute("SELECT name, uid, logged_in FROM users")
        users = c.fetchall()

        content += ["<table>"]
        content += ["<tr><th>UID</th><th>Name</th><th>Logged In</th></tr>"]
        for k in users:
            content += ["<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(k[1], k[0], "Yes" if k[2] == 1 else "No")]

        content += ["</table>"]
    else:
        status = 401
        content += ["<a href='/login.html'>Please login</a>"]
    return status, content + timecard.html_end(), []


def fullview(c, environ):
    content = timecard.html_begin()
    status = 200

    if auth.verify_auth(c, environ):

        c.execute("SELECT name, uid, logged_in FROM users")
        users = c.fetchall()

        usermap = {}
        for k in users:
            usermap[k[1]] = User(k[1], k[0], k[2])

        c.execute("SELECT uid, date, event_type FROM events")
        events = c.fetchall()
        events = sorted(events, key=lambda x: x[1])

        content += ["<table>"]

        content += ["<tr><th>Name</th><th>Logged In</th><th>Time Spent (hh:mm:ss)</th></tr>"]
        for uid, user in usermap.items():
            sumtime = 0
            uevents = list(filter(lambda x: x[0] == uid, events))
            if len(uevents) % 2 != 0:
                now = datetime.datetime.now()
                sumtime += int(unix_time(now) -
                               unix_time(datetime.datetime.strptime(uevents[-1][1], config.timeformat)))
                uevents = uevents[:-1]
            for i in range(0, len(uevents), 2):
                login = uevents[i]
                logout = uevents[i + 1]
                timelogin = unix_time(datetime.datetime.strptime(login[1], config.timeformat))
                timelogout = unix_time(datetime.datetime.strptime(logout[1], config.timeformat))
                sumtime += timelogout - timelogin
            timespent = datetime.timedelta(seconds=sumtime)
            seconds = timespent.total_seconds()
            total_hours = int(seconds // 3600)
            seconds %= 3600
            minutes = int(seconds // 60)
            seconds %= 60
            content += ["<tr><td>{name}</td><td>{logged_in}<td>{hh}:{mm}:{ss}</td>"
                        "<td><button class='do-login' data-user='{name}'>Login</button></td>"
                        "<td><button class='do-logout' data-user='{name}'>Logout</button></td></tr>"
                        .format(name=user.name,
                                logged_in=("Yes" if user.logged_in == 1 else "No"),
                                hh=total_hours,
                                mm=minutes,
                                ss=int(seconds))]

        content += ["</table>"]
        content += ["""<script type="text/javascript">
        req = function(type, name) {
            $.post("/app/action/" + type, {"name": name, "plain": true}, function() {
                location.reload();
            }).fail(function(jqXHR) {
                alert("Failed to " + type + " " + name + ". Server says: " + jqXHR.responseText);
            });
        };

        $(".do-login").click(function() {
            req("login", $(this).data("user"));
        });
        $(".do-logout").click(function() {
            req("logout", $(this).data("user"));
        });
        </script>"""]
    else:
        status = 401
        content += ["<a href='/login.html'>Please login</a>"]
    return status, content + timecard.html_end(), []


def timeview(c, environ):
    content = timecard.html_begin()
    status = 200

    if auth.verify_auth(c, environ):

        c.execute("SELECT name, uid, logged_in FROM users")
        users = c.fetchall()

        usermap = {}
        for k in users:
            usermap[k[1]] = User(k[1], k[0], k[2])

        c.execute("SELECT uid, date, event_type FROM events")
        events = c.fetchall()
        events = sorted(events, key=lambda x: x[1])

        content += ["<table>"]

        content += ["<tr><th>Name</th><th>Time Spent (hh:mm:ss)</th></tr>"]
        for uid, user in usermap.items():
            sumtime = 0
            uevents = list(filter(lambda x: x[0] == uid, events))
            if len(uevents) % 2 != 0:
                now = datetime.datetime.now()
                sumtime += int(unix_time(now) -
                               unix_time(datetime.datetime.strptime(uevents[-1][1], config.timeformat)))
                uevents = uevents[:-1]
            for i in range(0, len(uevents), 2):
                login = uevents[i]
                logout = uevents[i + 1]
                timelogin = unix_time(datetime.datetime.strptime(login[1], config.timeformat))
                timelogout = unix_time(datetime.datetime.strptime(logout[1], config.timeformat))
                sumtime += timelogout - timelogin
            timespent = datetime.timedelta(seconds=sumtime)
            seconds = timespent.total_seconds()
            total_hours = int(seconds // 3600)
            seconds %= 3600
            minutes = int(seconds // 60)
            seconds %= 60
            content += ["<tr><td>{}</td><td>{}:{}:{}</td></tr>".format(user.name, total_hours, minutes, int(seconds))]

        content += ["</table>"]
    else:
        status = 401
        content += ["<a href='/login.html'>Please login</a>"]
    return status, content + timecard.html_end(), []
