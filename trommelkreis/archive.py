from datetime import date, datetime, timedelta
from string import punctuation
from itertools import groupby

from random import randint

class AudioFile():
    def __init__(self):
        self.name = "filename" + str(randint(1, 999)) + ".mp3"
        self.author = "fshstk"
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

    def get_file_by_name(self, filename):
        for file in self.files:
            if file.name == filename:
                return file
        else:
            return None

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