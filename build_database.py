import os
import json
import sqlalchemy.exc
from datetime import datetime

from trommelkreis.archive import *
from trommelkreis import db

ARCHIVE_PATH = "/Users/fshstk/Documents/Digitaler Trommelkreis/website/archive/sessions"
UPLOAD = False
ERASE_ALL = False

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
        sesh.name = seshinfo["session yyyymmdd"]
        if seshname != sesh.name:
            print("ERROR: mismatch between folder name and sessioninfo.json")
            continue
        sesh.date = datetime.strptime(sesh.name, "%Y%m%d").date()
        sesh.challenge.name = seshinfo["challenge name"]
        sesh.challenge.blurb = seshinfo["challenge text short"]
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
        print("Aborted")
        print("ERROR: {}".format(e.args[0]))

    if UPLOAD:
        for trackname in tracks:
            if not trackname.endswith(".mp3"):
                print(
                    "----> WARNING: skipped file {} (doesn't end with .mp3)".format(
                        trackname
                    )
                )
                continue

            trackpath = os.path.join(filedir, trackname)
            # The following line raises an IntegrityError when trying to add existing artist to database ?!:
            track = AudioFile.from_mp3(trackpath)
            sesh.files.append(track)
            print(
                "----> Uploading {}... ({})".format(
                    track.filename, track.filesize_string
                ),
                end=" ",
                flush=True,
            )
            db.session.commit()
            print("Done")

        successful_uploads += 1

print(separator)

print(
    "{} of {} sessions successfully uploaded".format(
        successful_uploads, len(sessionlist)
    )
)
