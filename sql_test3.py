from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import deferred
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
from mutagen.mp3 import EasyMP3
import os.path

app = Flask(__name__)
# Disabled to suppress warning at startup:
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{user}:{password}@{host}/{db}".format(
    user="trommelkreis",
    password="YUM-senk8nect",
    host="data.trommelkreis.club",
    db="trommelkreis_test",
)
db = SQLAlchemy(app)


class AudioFile(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    # Required:
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False)
    filename = db.Column(db.Unicode(255), nullable=False)
    filesize = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    data = deferred(db.Column(db.LargeBinary(length=(1e8)), nullable=False))  # 100 MB
    # Optional:
    trackname = db.Column(db.Unicode(255), nullable=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=True)

    @classmethod
    def from_mp3(cls, filepath, artistname=None):
        # TODO: check if (a) import works, (b) artist tag is updated
        # TODO: check if it works without session argument if using Session.files.append()
        mp3 = EasyMP3(filepath)
        filename = os.path.basename(filepath)

        if mp3.info.sketchy:
            raise ValueError("input file may not be a valid MP3")

        # If we pass in a value for artist, write it to the MP3 metadata:
        if artistname is not None:
            mp3["artist"][0] = artistname
            mp3.save()
        # Else, check for artist tag in metadata and use that instead:
        elif "artist" in mp3:
            artistname = mp3["artist"][0]

        # If MP3 contains title tag, use this as trackname:
        if "title" in mp3:
            trackname = mp3["title"][0]
        # Else use the filename without the suffix:
        else:
            trackname = os.path.splitext(filename)[0]

        with open(filepath, "rb") as fileobj:
            data = fileobj.read()

        if artistname is not None:
            try:
                artist = Artist.query.filter_by(name=artistname).one()
            except NoResultFound:
                artist = Artist(name=artistname)

        return AudioFile(
            filename=filename,
            filesize=len(data),
            data=data,
            duration=round(mp3.info.length),
            artist=artist,
            trackname=trackname,
        )

    def __repr__(self):
        return "<AudioFile: {name} [{size}]>".format(
            name=self.filename if self.filename is not None else "??",
            size=self.filesize_string if self.filesize is not None else "??",
        )

    def __len__(self):
        return self.filesize

    @hybrid_property
    def filesize_string(self):
        kB = 1000
        MB = kB ** 2
        if self.filesize > MB:
            return "{:.2f} MB".format(self.filesize / MB)
        else:
            return "{:.0f} kB".format(self.filesize / kB)

    @hybrid_property
    def duration_string(self):
        return "{:02d}:{:02d}".format(self.duration // 60, self.duration % 60)


class Session(db.Model):
    __tablename__ = "sessions"
    id = db.Column(db.Integer, primary_key=True)
    # Required:
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)  # unique?
    # Generated:
    files = db.relationship("AudioFile", backref="session", lazy=True)

    def __repr__(self):
        return "<Session: {} [{} file(s)]>".format(self.date, len(self.files))


class Artist(db.Model):
    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key=True)
    # Required:
    name = db.Column(db.Unicode(255), nullable=False, unique=True)
    # Generated:
    files = db.relationship("AudioFile", backref="artist", lazy=True)

    def __repr__(self):
        return "<Artist: {} [{} track(s)]>".format(self.name, len(self.files))


class Challenge(db.Model):
    __tablename__ = "challenges"
    id = db.Column(db.Integer, primary_key=True)
    # Required:
    name = db.Column(db.Unicode(255), nullable=False, unique=True)
    # Optional:
    text_short = db.Column(db.Unicode(1023), nullable=True)
    text_long = db.Column(db.Unicode(4095), nullable=True)
    # Generated:
    sessions = db.relationship("Session", backref="challenge", lazy=True)

    def __repr__(self):
        return "<Challenge: {name} [{num_sessions}]>".format(
            name=self.name,
            num_sessions="UNUSED"
            if len(self.sessions) == 0
            else "used in {} session(s)".format(len(self.sessions)),
        )


# Drop into interactive shell for debugging:
if __name__ == "__main__":
    REBUILD = True

    if REBUILD:
        db.drop_all()
        db.create_all()

        # Create some test data:
        a = Artist(name="Alice")
        b = Artist(name="Alices")
        c = Challenge(name="Foo", text_short="This is a test challenge.")
        x = Session(date=datetime.now(), challenge=c)

        for row in [a, b, c, x]:
            db.session.add(row)

        # f1 = AudioFile.from_mp3(
        #     "/Users/fshstk/Downloads/joe_der_singende_staubsauger.mp3"
        # )
        f2 = AudioFile.from_mp3("/Users/fshstk/Downloads/41 Skeng.mp3")

        # x.files.append(f1)
        x.files.append(f2)

        db.session.commit()

    import IPython

    IPython.embed()
