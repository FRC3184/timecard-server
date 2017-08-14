import sqlite3
import config
import auth
import action
import status
import view_calendar
from urllib.parse import parse_qs
import sys


def get_location_header(path):
    return "Location", path


def get_data(environ):
    method = environ["REQUEST_METHOD"].upper()
    if method == "GET":
        return parse_get(environ)
    elif method == "POST":
        return parse_post(environ)
    else:
        return None  # idk


def parse_get(environ):
    return parse_qs(environ['QUERY_STRING'], True)


def parse_post(environ):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0
    return parse_qs(environ['wsgi.input'].read(request_body_size))


status_str = {
    200: "200 OK",
    303: "303 See Other",
    400: "400 Bad Request",
    401: "401 Unauthorized",
    404: "404 Not Found"
}


def html_begin(title="Timecard", css=""):
    return \
            ["""<!DOCTYPE html>
            <html>
            <head>
                <title>{_title}</title>
                <link rel="stylesheet" type="text/css" href="/css/main.css" />
                <style type="text/css">
                    {_css}
                </style>
                <script src="https://code.jquery.com/jquery-3.1.0.min.js"
                 integrity="sha256-cCueBR6CsyA4/9szpPfrX3s49M9vUU5BgtiJj06wt/s="
                 crossorigin="anonymous"></script>
            </head>
            <body>
            """.format(_title=title, _css=css)]


def html_end():
    return ["</body>\n</html>"]


def default(c, environ):
    return 303, ["Hi!"], []


def error(c, environ):
    return 404, ["404: Go away"], []


def application(environ, start_response):
    handler_dict = {
        "": default,
        "manage": status.fullview,
        "auth": {
            "login": auth.login,
            "logout": auth.logout
        },
        "action": {
            "gen_barcode": action.gen_barcode,
            "login": action.login,
            "logout": action.logout,
            "create": action.create_user
        },
        "status": {
            "events": status.events,
            "time": status.timeview,
            "view": status.view,
            "calendar": view_calendar.calendar_view
        }
    }

    db = sqlite3.connect(config.timecard_db)
    c = db.cursor()

    # Find function
    url = environ["PATH_INFO"]
    if url.endswith("/"):
        url = url[:-1]
    if url.startswith("/"):
        url = url[1:]
    if len(url) == 0:
        url = "/"
    path = url.split("/")
    app = handler_dict
    try:
        for k in path:
            app = app[k]
    except (KeyError, TypeError):
        app = error

    status_code, content, headers = app(c, environ)

    db.commit()
    db.close()

    content = "\n".join(content).encode()

    headers += [("Content-Type", "text/html")]
    start_response(status_str[status_code], headers)
    return [content]
