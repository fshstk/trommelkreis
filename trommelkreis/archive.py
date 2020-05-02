from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import deferred
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
import urllib.parse
from itertools import groupby
from mutagen.mp3 import EasyMP3
import os.path

if __name__ == "__main__":
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy

    REBUILD = True
    POPULATE_WITH_TEST_DATA = False

    app = Flask(__name__)
    # Disabled to suppress warning at startup:
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "mysql://{user}:{password}@{host}/{db}".format(
        user="trommelkreis",
        password="YUM-senk8nect",
        host="data.trommelkreis.club",
        db="trommelkreis",
    )
    db = SQLAlchemy(app)
else:
    from . import app, db


class AudioFile(db.Model):
    __tablename__ = "files"
    __table_args__ = (UniqueConstraint("session_id", "slug"),)
    id = db.Column(db.Integer, primary_key=True)

    @staticmethod
    def generate_slug(context):
        """Generate url-safe string from filename column."""
        # TODO: generate "_2" or something else if not unique?
        filename = context.get_current_parameters()["filename"]
        return urllib.parse.quote(filename)

    # Required:
    # TODO: boolean to see if file/session is CC-licensed?
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False)
    title = db.Column(db.Unicode(255), nullable=False)
    filename = db.Column(db.Unicode(255), nullable=False)
    slug = db.Column(db.Unicode(255), nullable=False, default=generate_slug.__func__)
    filesize = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    data = deferred(db.Column(db.LargeBinary(length=(30e6)), nullable=False))
    # Optional:
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=True)

    @classmethod
    def from_mp3(cls, filepath, artistname=None):
        mp3 = EasyMP3(filepath)
        filename = os.path.basename(filepath)

        if mp3.info.sketchy:
            raise ValueError("input file may not be a valid MP3")

        # If we pass in a value for artist, write it to the MP3 metadata:
        # (overwrite any existing tag)
        if artistname is not None:
            mp3["artist"] = artistname
            mp3.save()
        # Else, check for artist tag in metadata and use that instead:
        elif "artist" in mp3:
            artistname = mp3["artist"][0]

        # If MP3 contains title tag, use this as name:
        if "title" in mp3:
            title = mp3["title"][0]
        # Else use the filename without the suffix:
        else:
            title = os.path.splitext(filename)[0]

        with open(filepath, "rb") as fileobj:
            data = fileobj.read()

        if artistname is not None:
            try:
                artist = Artist.query.filter_by(name=artistname).one()
            except NoResultFound:
                artist = Artist(name=artistname)
        else:
            artist = None

        return AudioFile(
            filename=filename,
            filesize=len(data),
            data=data,
            duration=round(mp3.info.length),
            artist=artist,
            title=title,
        )

    def __repr__(self):
        return "<AudioFile: {name} [{size}]>".format(
            name=self.filename if not None else "??",
            size=self.filesize_string if self.filesize is not None else "??",
        )

    def __str__(self):
        return self.slug

    def __len__(self):
        return self.filesize

    @staticmethod
    def readable_filesize(numbytes):
        kB = 1000
        MB = kB ** 2
        if numbytes > MB:
            return "{:.2f} MB".format(numbytes / MB)
        else:
            return "{:.0f} kB".format(numbytes / kB)

    @property
    def filesize_string(self):
        return self.readable_filesize(self.filesize)

    @property
    def duration_string(self):
        return "{:02d}:{:02d}".format(self.duration // 60, self.duration % 60)


class Session(db.Model):
    __tablename__ = "sessions"
    id = db.Column(db.Integer, primary_key=True)

    @staticmethod
    def generate_slug(context):
        """Generate url-safe string from date column."""
        date = context.get_current_parameters()["date"]
        return date.strftime("%Y%m%d")

    # Required:
    # TODO: boolean to see if file/session is CC-licensed?
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    slug = db.Column(
        db.Unicode(255), nullable=False, unique=True, default=generate_slug.__func__
    )
    # Generated:
    files = db.relationship("AudioFile", backref="session", lazy=True)

    def __repr__(self):
        return "<Session: {} [{} file(s)]>".format(self.slug, len(self.files))

    def __str__(self):
        return self.slug

    @classmethod
    def from_slug(cls, slug):
        return cls.query.filter_by(slug=slug).one()

    @classmethod
    def grouped_by_month(cls):
        sessions = Session.query.order_by(Session.date).all()
        grouped_sessions = []
        for _, group in groupby(sessions, key=lambda x: x.monthyear):
            grouped_sessions.append(list(group))
        return grouped_sessions

    @property
    def month(self):
        return self.date.strftime("%B")

    @property
    def year(self):
        return self.date.strftime("%Y")

    @property
    def monthyear(self):
        return self.date.strftime("%B %Y")

    @property
    def datestring(self):
        return self.date.strftime("%d.%m.%Y")

    @property
    def filecount_string(self):
        filecount = len(self.files)
        if filecount is 0:
            return "Keine Einträge"
        elif filecount is 1:
            return "1 Eintrag"
        else:
            return "{} Einträge".format(filecount)

    def get_file_by_slug(self, slug):
        # do this again since flask undoes it? feels hacky (TODO)
        slug = urllib.parse.quote(slug)
        return AudioFile.query.filter_by(session=self, slug=slug).one()


class Artist(db.Model):
    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key=True)
    # Required:
    name = db.Column(db.Unicode(255), nullable=False, unique=True)
    # Generated:
    files = db.relationship("AudioFile", backref="artist", lazy=True)

    def __repr__(self):
        return "<Artist: {} [{} track(s)]>".format(self.name, len(self.files))

    def __str__(self):
        return self.name


class Challenge(db.Model):
    __tablename__ = "challenges"
    id = db.Column(db.Integer, primary_key=True)
    # Required:
    name = db.Column(db.Unicode(255), nullable=False, unique=True)
    # Optional:
    blurb = db.Column(db.Unicode(1023), nullable=True)
    markdown = db.Column(db.Unicode(4095), nullable=True)
    # Generated:
    sessions = db.relationship("Session", backref="challenge", lazy=True)

    def __repr__(self):
        return "<Challenge: {name} [{num_sessions}]>".format(
            name=self.name,
            num_sessions="UNUSED"
            if len(self.sessions) == 0
            else "{} session(s)".format(len(self.sessions)),
        )

    def __str__(self):
        return self.name


# Drop into interactive shell for debugging:
if __name__ == "__main__":
    if REBUILD:
        db.drop_all()
        db.create_all()

    if POPULATE_WITH_TEST_DATA:
        # Create some test data:
        a = Artist(name="Alice")
        b = Artist(name="Bob")
        c = Challenge(name="Foo", blurb="This is a test challenge.")
        d = Challenge(name="Bar", blurb="This is another test challenge.")
        x = Session(date=datetime.now(), challenge=c)
        y = Session(date=datetime.now(), name="20200424_bonus", challenge=c)

        for row in [a, b, c, d, x]:
            db.session.add(row)

        # f1 = AudioFile.from_mp3(
        #     "/Users/fshstk/Downloads/joe_der_singende_staubsauger.mp3",
        #     artistname="fshstk",
        # )
        # f2 = AudioFile.from_mp3("/Users/fshstk/Downloads/41 Skeng.mp3")

        # x.files.append(f1)
        # x.files.append(f2)

        db.session.commit()

    import IPython

    IPython.embed()
