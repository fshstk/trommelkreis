import mysql.connector
from datetime import datetime

# from cached_property import cached_property


class DatabaseObject:
    sql_host = "data.trommelkreis.club"
    sql_db = "trommelkreis"

    # User only has SELECT/INSERT access:
    sql_user = "trommelkreis_api"
    sql_pass = "scan1ken_PLIF"

    # TODO: context manager?
    db = mysql.connector.connect(
        host=sql_host, user=sql_user, passwd=sql_pass, database=sql_db
    )
    cursor = db.cursor()

    def __init__(self, id):
        self.id = id

    @classmethod
    def create(cls, data):
        raise NotImplementedError("this method should be overriden by child classes")

    @classmethod
    def all(cls, limit=1000):
        cls.cursor.execute(
            "SELECT {} FROM {} LIMIT {}".format(cls.idstring, cls.table, limit)
        )
        objects = []
        for id in cls.unpack(cls.cursor.fetchall()):
            objects.append(cls(id))
        return objects

    @classmethod
    def query(cls, attributes, table, key, val, limit=1000):
        cls.cursor.execute(
            "SELECT {} FROM {} WHERE {}={} LIMIT {}".format(
                attributes, table, key, val, limit
            )
        )
        return cls.unpack(cls.cursor.fetchall())

    def column(self, col, table=None, limit=1):
        if table is None:
            table = self.table
        self.cursor.execute(
            "SELECT {} FROM {} WHERE {}={} LIMIT {}".format(
                col, table, self.idstring, self.id, limit
            )
        )
        return self.unpack(self.cursor.fetchall())

    @classmethod
    def unpack(cls, response):
        result = []
        for item in response:
            (item,) = item
            result.append(item)
        return result


class AudioFile(DatabaseObject):
    table = "files"
    idstring = "file_id"

    def __repr__(self):
        return self.filename

    def __len__(self):
        return self.filesize

    @classmethod
    def create(cls, data):
        # TODO
        raise NotImplementedError

    @property
    def binary_data(self):
        # NOTE: Could be Null
        return self.column("data")[0]

    @property
    def filename(self):
        return self.column("filename")[0]

    @property
    def trackname(self):
        # NOTE: Could be Null
        name = self.column("trackname")[0]
        if name is not None:
            return name
        else:
            return self.filename

    @property
    def duration(self):
        return self.column("duration_seconds")[0]

    @property
    def duration_string(self):
        # Cache duration to avoid multiple database queries:
        duration = self.duration
        return "{:02d}:{:02d}".format(duration // 60, duration % 60)

    @property
    def filesize(self):
        # NOTE: Could be Null (if self.data is None)
        filesize = self.column("filesize_bytes")[0]
        if filesize is not None:
            return filesize
        else:
            return 0

    @property
    def filesize_string(self):
        # Cache filesize to avoid multiple database queries:
        filesize = self.filesize
        kB = 1000
        MB = kB ** 2
        if filesize > MB:
            return "{:.2f} MB".format(filesize / MB)
        else:
            return "{:.0f} kB".format(filesize / kB)

    @property
    def artist(self):
        # NOTE: Could be Null
        artist_id = self.column("artist_id")[0]
        if artist_id is not None:
            return Artist(artist_id)
        else:
            return None


class Session(DatabaseObject):
    table = "sessions"
    idstring = "session_id"

    def __repr__(self):
        return self.date.strftime("%Y%m%d")

    def __len__(self):
        return len(self.files)

    @classmethod
    def fromdate(cls, date):
        # NOTE: Returns list, potentially with zero or multiple entries.
        # NOTE: This works with both datetime objects and strings. Neat!
        idlist = cls.query(cls.idstring, cls.table, "date", "'{}'".format(date))
        sessions = []
        for id in idlist:
            sessions.append(Session(id))
        return sessions

    @classmethod
    def create(cls, data):
        # TODO
        raise NotImplementedError

    @property
    def challenge(self):
        # NOTE: Could be Null
        challenge_id = self.column("challenge_id")[0]
        if challenge_id is not None:
            return Challenge(challenge_id)
        else:
            return None

    @property
    def date(self):
        return self.column("date")[0]

    @property
    def files(self):
        results = self.column(AudioFile.idstring, table=AudioFile.table, limit=100)
        files = []
        for id in results:
            files.append(AudioFile(id))
        return files


class Artist(DatabaseObject):
    table = "artists"
    idstring = "artist_id"

    def __repr__(self):
        return self.name

    @classmethod
    def create(cls, data):
        # TODO
        raise NotImplementedError

    @property
    def name(self):
        return self.column("name")[0]

    @property
    def files(self):
        # TODO: untested
        results = self.column(AudioFile.idstring, table=AudioFile.table, limit=100)
        files = []
        for id in results:
            files.append(AudioFile(id))
        return files


class Challenge(DatabaseObject):
    table = "challenges"
    idstring = "challenge_id"

    def __repr__(self):
        return self.name

    @classmethod
    def fromname(cls, name):
        # NOTE: Guaranteed to be unique in database.
        # TODO: untested
        idlist = cls.query(cls.idstring, cls.table, "name", name)
        if len(idlist) != 0:
            return Challenge(idlist[0])
        else:
            raise KeyError("no challenge named {}".format(name))

    @classmethod
    def create(cls, data):
        # TODO
        raise NotImplementedError

    @property
    def name(self):
        # NOTE: Could be Null
        name = self.column("name")[0]
        if name is not None:
            return name
        else:
            return "<untitled>"

    @property
    def text_short(self):
        # NOTE: Could be Null
        text = self.column("text_short")[0]
        if text is not None:
            return text
        else:
            return ""

    @property
    def text_long(self):
        # NOTE: Could be Null
        text = self.column("text_long")[0]
        if text is not None:
            return text
        elif self.text_short is not None:
            return self.text_short
        else:
            return "<p>Zu dieser Challenge sind keine Infos verfügbar.</p>"
