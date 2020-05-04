import os
import json
import sqlalchemy.exc
from datetime import datetime
import IPython

from trommelkreis.archive import *
from trommelkreis import db

ARCHIVE_PATH = "/Users/fshstk/Documents/Digitaler Trommelkreis/website/archive/sessions"
ERASE_ALL = True

sessionlist = next(os.walk(ARCHIVE_PATH))[1]
sessionlist.sort()
successful_uploads = 0
separator = "--------------------------------------------"

if ERASE_ALL:
    if input("Are you SURE you want to delete the entire database? (y) ") == "y":
        print("Rebuilding database...", end=" ", flush=True)
        db.drop_all()
        db.create_all()
        print("Done")
    else:
        print("Aborting database rebuild")

for seshname in sessionlist:
    print(separator)
    print("Adding session {}...".format(seshname))

    sesh = Session(challenge=Challenge())
    seshpath = os.path.join(ARCHIVE_PATH, seshname)
    markdownfile = os.path.join(seshpath, "challenge.md")
    infofile = os.path.join(seshpath, "sessioninfo.json")
    filedir = os.path.join(seshpath, "files")

    try:
        with open(infofile) as f:
            seshinfo = json.load(f)
    except FileNotFoundError:
        print("ERROR: missing sessioninfo.json".format(seshname))
        continue
    except json.decoder.JSONDecodeError:
        print("ERROR: malformed or unreadable sessioninfo.json")
        continue

    try:
        if seshname != seshinfo["session yyyymmdd"]:
            print("ERROR: mismatch between folder name and sessioninfo.json")
            continue
        sesh.date = datetime.strptime(seshname, "%Y%m%d")
        sesh.challenge.name = seshinfo["challenge name"]
        sesh.challenge.blurb = seshinfo["challenge text short"]
        # sesh.challenge.kosher = seshinfo["copyright issues y/n"]
    except KeyError as e:
        print("ERROR: missing key {}".format(e.args[0]))
        continue

    print("Challenge: {}".format(sesh.challenge.name))

    try:
        with open(markdownfile) as f:
            sesh.challenge.markdown = f.read()
    except FileNotFoundError:
        print("WARNING: missing challenge.md")

    if os.path.isdir(filedir):
        tracks = next(os.walk(filedir))[2]
    else:
        print("WARNING: no files directory")
        continue

    print("Adding session to database...", end=" ", flush=True)
    try:
        db.session.add(sesh)
        db.session.commit()
        print("Done")
    except sqlalchemy.exc.IntegrityError as e:
        db.session.rollback()
        print("Aborted")
        print("ERROR: {}".format(e.args[0]))
        continue

    for trackname in tracks:
        if not trackname.endswith(".mp3"):
            print(
                "----> WARNING: skipped file {} (doesn't end with .mp3)".format(
                    trackname
                )
            )
            continue

        trackpath = os.path.join(filedir, trackname)
        track = AudioFile.from_mp3(trackpath)

        # TODO: sesh.files.append(track) sometimes raises the following error:
        # (MySQLdb._exceptions.OperationalError) (1048, "Column 'session_id' cannot be null")
        # Calling db.session.rollback() and trying again fixes the issue. (Why?)
        # Additionally, "SQL Server has gone away" type exception occurs when uploading large (>15MB?) files.
        try:
            print(
                "----> Add {} ... ({})".format(track.filename, track.filesize_string),
                end=" ",
                flush=True,
            )
            # with db.session.no_autoflush:
            sesh.files.append(track)
            # db.session.flush()
            db.session.commit()
            print("Done")
        except Exception as e:
            print("Aborted")
            print("ERROR: {}".format(e))
            IPython.embed()  # error launches debugging shell

print(separator)
