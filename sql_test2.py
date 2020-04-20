import mysql.connector
from datetime import datetime
from cached_property import cached_property

sql_host = "data.trommelkreis.club"
sql_user = "trommelkreis"
sql_pass = "firm!TWAD5baub"
sql_db = "trommelkreis"

db = mysql.connector.connect(
    host=sql_host, user=sql_user, passwd=sql_pass, database=sql_db
)
cursor = db.cursor()


# first session:
cursor.execute(
    """
    SELECT date
    FROM sessions
    ORDER BY date
    LIMIT 1"""
)
(first_session,) = cursor.fetchone()
print(first_session)
print(type(first_session))
formatted_date = first_session.strftime("%Y-%m-%d")

cursor.execute(
    """
    SELECT a.file_id
    FROM files a
    WHERE a.session_id in
    (select b.session_id from sessions b where b.date="{}");
    """.format(
        formatted_date
    )
)
tracks = cursor.fetchall()

for track in tracks:
    print(track)


################################################################################


class DatabaseObject:
    def __init__(self, id):
        self.id = id
        # TODO: move cursor/db creation here

    def column(self, col):
        # TODO: add context manager?
        # TODO: rename columns from xxx_id to id
        cursor.execute("SELECT {} FROM files WHERE {}_id={}".format(col, self.id))
        (result,) = cursor.fetchone()
        # TODO: handle multiple results


class AudioFile(DatabaseObject):
    @property
    def binary_data(self):
        return self.column("data")

    @cached_property
    def filename(self):
        return self.column("filename")

    @cached_property
    def trackname(self):
        return self.column("trackname")

    @cached_property
    def duration(self):
        # TODO: maybe do some formatting here? use this as __len__?
        return self.column("duration_seconds")

    @cached_property
    def filesize(self):
        # TODO: maybe do some formatting here? use this as __len__?
        return self.column("filesize_bytes")

    @cached_property
    def artist(self):
        # TODO
        raise NotImplementedError


class Session(DatabaseObject):
    @cached_property
    def challenge(self):
        challenge_id = self.column("challenge_id")
        return Challenge(challenge_id)

    @cached_property
    def date(self):
        # TODO: formatting?
        return self.column("date")

    @cached_property
    def files(self):
        # TODO
        raise NotImplementedError


class Artist(DatabaseObject):
    @cached_property
    def name(self):
        return self.column("name")

    @cached_property
    def files(self):
        # TODO
        raise NotImplementedError


class Challenge(DatabaseObject):
    @cached_property
    def title(self):
        return self.column("name")

    @cached_property
    def text_short(self):
        return self.column("text_short")

    @cached_property
    def text_long(self):
        return self.column("text_long")
