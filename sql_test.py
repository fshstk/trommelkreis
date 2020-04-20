from sqlalchemy import create_engine, MetaData, ForeignKey
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, LargeBinary, Date

from sqlalchemy.ext.declarative import declarative_base

sql_host = "data.trommelkreis.club"
sql_user = "trommelkreis"
sql_pass = "firm!TWAD5baub"
sql_db = "trommelkreis_test"

sql_url = "mysql://{}:{}@{}/{}".format(sql_user, sql_pass, sql_host, sql_db)

engine = create_engine(sql_url)
engine.echo = True  # debug
connection = engine.connect()

meta = MetaData()

Base = declarative_base()


class Challenges(Base):
    __tablename__ = "challenges"
    challenge_id = Column(Integer, primary_key=True)
    name = Column(String)
    text_short = Column(String)
    text_html = Column(String)


class Sessions(Base):
    __tablename__ = "sessions"
    session_id = Column(Integer, primary_key=True)
    challenge_id = Column(Integer, ForeignKey("challenges.challenge_id"))
    date = Column(Date)


class Files(Base):
    __tablename__ = "files"
    file_id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.session_id"))
    filename = Column(String)
    data = Column(LargeBinary)
    trackname = Column(String)
    artist = Column(String)
    duration_seconds = Column(Integer)
    filesize_bytes = Column(Integer)
