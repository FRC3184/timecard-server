import timecard
import datetime
import calendar


def calendar_view(c, environ):
    cal = calendar.HTMLCalendar(calendar.SUNDAY)
    html = cal.formatmonth(datetime.datetime.now().year, datetime.datetime.now().month)

    return 200, timecard.html_begin() + [html] + timecard.html_end(), []
