# Disabled to suppress warning at startup:
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = "mysql://{user}:{password}@{host}/{db}".format(
    user="trommelkreis",
    password="YUM-senk8nect",
    host="data.trommelkreis.club",
    db="trommelkreis",
)
