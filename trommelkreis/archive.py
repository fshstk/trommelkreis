import os
from datetime import date, datetime, timedelta
from string import punctuation
from itertools import groupby
from mutagen.mp3 import EasyMP3
import math

from .config import ARCHIVE_PATH

class AudioFile():
    def __init__(self, path):
        self.mp3 = EasyMP3(path)
        self.path = path
        if self.mp3.info.sketchy:
            raise ValueError("sketchy mp3") # or whatever error is most appropriate

        if "title" in self.mp3:
            self.name = self.mp3["title"]
        else:
            self.name = os.path.basename(self.path)
        if "artist" in self.mp3:
            self.artist = self.mp3["artist"]
        else:
            self.artist = ""

        # TODO: properties:
        self.duration = timedelta(seconds = math.floor(self.mp3.info.length))
        self.size = os.path.getsize(self.path) # TODO: MB

class Session():
    max_challenge_length = 100
    date_output_format = "%d.%m.%Y"

    def __init__(self, datestring, name = None, challenge = ""):
        self.date = datetime.strptime(datestring, "%Y%m%d").date() # yyyymmdd
        if name is None:
            self.name = datestring
        else:
            self.name = name
        self.challenge = challenge
        self.files = []

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
        tree = os.walk(ARCHIVE_PATH)
        directories = next(tree)[1]

        # get a list of all top level directories and parse the dates
        for directory in directories:
            try:
                self.sessions.append(Session(directory))
            except ValueError:
                directories.remove(directory) # prune all directories that can't be parsed

        for session in self.sessions:
            _, subdirectories, files = next(tree)

            if "challenge.txt" in files:
                # session.name = blah
                # session.challenge = blah
                pass

            if "files" in subdirectories:
                subdirectories = ["files"] # ignore everything except files directory

                path, _, tracks = next(tree)

                for trackname in tracks:
                    trackpath = os.path.join(path, trackname)
                    try:
                        track = AudioFile(trackpath)
                    except:
                        continue
                    session.files.append(track)
            else:
                subdirectories = []

    def init_with_placeholder_data(self):
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