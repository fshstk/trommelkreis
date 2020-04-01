from flask import Flask, render_template, request, abort
from itertools import groupby
import locale

locale.setlocale(locale.LC_ALL, "de_AT.UTF-8")
app = Flask(__name__)

################################################################################

from datetime import date, datetime, timedelta
from string import punctuation

class AudioFile():
    def __init__(self):
        self.name = "filename"
        self.size = "1.51 MB"
        self.duration = timedelta(seconds = 135)

class Session():
    max_challenge_length = 100
    date_output_format = "%d.%m.%Y"

    def __init__(self, datestring):
        # example data:
        self.name = "Kurt Razelli Challenge"
        # self.date = date.now()
        # self.date = datetime.strptime(datestring, "%Y%m%d").date() # yyyymmdd
        self.date = datestring
        self.challenge = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce quis augue iaculis, tempor orci non, porta justo. Pellentesque nisi ex, ultrices eget cursus at, fringilla in libero. Ut euismod libero at eros porttitor, in rhoncus augue pellentesque. Quisque auctor nibh pretium elit facilisis feugiat. Cras rhoncus magna sed magna aliquet cursus. Sed et varius quam. Fusce feugiat dolor ac neque hendrerit, non gravida justo aliquet. Donec venenatis vel neque sed consequat. Morbi scelerisque tempus diam. Maecenas ullamcorper laoreet iaculis."
        self.files = []
        for _ in range(7):
            self.files.append(AudioFile())

    @property
    def count(self):
        return len(self.files)

    @property
    def countstring(self):
        if self.count is 0:
            return "Keine Einträge"
        elif self.count is 1:
            return "1 Eintrag"
        else:
            return str(self.count) + " Einträge"

    @property
    def challenge_short(self):
        if len(self.challenge) > self.max_challenge_length:
            challenge_short = self.challenge[:self.max_challenge_length]
            while challenge_short[-1] in punctuation:
                self.challenge = self.challenge[:-1]
            return self.challenge[:self.max_challenge_length] + "…"
        else:
            return self.challenge

    @property
    def datestring(self):
        return self.date.strftime(self.date_output_format)

    @property
    def yyyymmdd(self):
        return self.date.strftime("%Y%m%d")

    @property
    def month(self):
        return self.date.strftime("%B")

    @property
    def year(self):
        return self.date.strftime("%Y")

    @property
    def monthyear(self):
        return self.date.strftime("%B %Y")

class SessionCollection():
    def __init__(self):
        self.sessions = []
        for i in range(20):
            self.sessions.append(Session((datetime.strptime("20190101", "%Y%m%d")-timedelta(days = 4*i)).date()))

    @property
    def sorted_by_date(self):
        return sorted(self.sessions, key = lambda x: x.date)

    @property
    def grouped_by_month(self):
        sessions = self.sorted_by_date
        grouped_sessions = []
        for _, group in groupby(sessions, key = lambda x: x.monthyear):
            grouped_sessions.append(list(group))
        return grouped_sessions

    @property
    def count(self):
        return len(self.sessions)

    def get_session_by_yyyymmdd(self, input):
        for session in self.sessions:
            if session.yyyymmdd == str(input):
                return session
        else:
            return None
            
################################################################################

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.jinja')

@app.route('/info')
def info():
    return render_template('info.jinja')

@app.route('/archiv')
@app.route('/archiv/')
def archive():
    return render_template('archive.jinja', archive = sessions.grouped_by_month)

@app.route('/upload')
def upload():
    return render_template('upload.jinja')

@app.route('/abo')
def subscribe():
    return render_template('subscribe.jinja')

@app.route('/challenge')
def challenge():
    return render_template('challenge.jinja')

@app.route('/archiv/<int:number>')
def session(number):
    session = sessions.get_session_by_yyyymmdd(number)
    if session is not None:
        return render_template('session.jinja', session = session)
    else:
        return abort(400)

@app.errorhandler(404) # possibly add more errors (403, 500)
def notfound(error):
    return render_template('error.jinja')

@app.errorhandler(400)
def badrequest(error):
    # return render_template('session_not_found.jinja', archive = sessions.grouped_by_month)
    return notfound(None)

################################################################################

sessions = SessionCollection()

@app.context_processor
def global_vars():
    return {}

################################################################################

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
