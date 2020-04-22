from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(
    "trommelkreis",  # user
    "YUM-senk8nect",  # password
    "data.trommelkreis.club",  # host
    "trommelkreis_test",  # db name
)
app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False  # Disabled tu suppress warning at startup.
db = SQLAlchemy(app)


class AudioFile(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=True)
    filename = db.Column(db.Unicode(255), nullable=False)
    trackname = db.Column(db.Unicode(255), nullable=True)
    data = db.Column(db.LargeBinary, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    filesize = db.Column(db.Integer, nullable=False)

    def __init__(self, file):
        session = None
        filename = None
        data = None
        duration = None
        artist = None  # optional
        trackname = None  # optional

        super().__init__(
            session=session,
            filename=filename,
            data=data,
            duration=duration,
            artist=artist,  # TODO: does this work for NoneType?
            trackname=trackname,  # TODO: does this work for NoneType?
        )

    def __repr__(self):
        return "<AudioFile: {}>".format(self.filename)

    def __len__(self):
        return self.filesize

    @hybrid_property
    def filesize_string(self):
        kB = 1000
        MB = kB ** 2
        if filesize > MB:
            return "{:.2f} MB".format(self.filesize / MB)
        else:
            return "{:.0f} kB".format(self.filesize / kB)

    @hybrid_property
    def duration_string(self):
        return "{:02d}:{:02d}".format(self.duration // 60, self.duration % 60)


class Session(db.Model):
    __tablename__ = "sessions"
    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)  # unique?

    files = db.relationship("AudioFile", backref="session", lazy=True)

    def __repr__(self):
        return "<Session: {}>".format(self.date)

    def __len__(self):
        # return self.files.count()  # does this work?
        # return len(self.files)  # or this?
        pass


class Artist(db.Model):
    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255), nullable=False, unique=True)

    files = db.relationship("AudioFile", backref="artist", lazy=True)

    def __repr__(self):
        return "<Artist: {}>".format(self.name)


class Challenge(db.Model):
    __tablename__ = "challenges"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255), nullable=False, unique=True)
    text_short = db.Column(db.Unicode(1023), nullable=True)
    text_long = db.Column(db.Unicode(4095), nullable=True)

    sessions = db.relationship("Session", backref="challenge", lazy=True)

    def __repr__(self):
        return "<Challenge: {}>".format(self.name)


# Drop into interactive shell for debugging:
if __name__ == "__main__":
    REBUILD = True

    if REBUILD:
        db.drop_all()
        db.create_all()

        # Create some test data:
        a = Artist(name="Alice")
        b = Artist(name="Bob")
        c = Challenge(name="Foo", text_short="This is a test challenge.")
        x = Session(date=datetime.now(), challenge=c)  # NOT challenge_id = c.id!

        for row in [a, b, c]:
            db.session.add(row)
        db.session.commit()

    import IPython

    IPython.embed()
