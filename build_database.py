import os
import json
import sqlalchemy.exc
from datetime import datetime

from trommelkreis.archive import *
from trommelkreis import db

ARCHIVE_PATH = "/Users/fshstk/Documents/Digitaler Trommelkreis/website/archive/sessions"
UPLOAD = True
ERASE_ALL = True

sessionlist = next(os.walk(ARCHIVE_PATH))[1]
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
        print("WARNING: missing challenge.md".format(seshname))

    if os.path.isdir(filedir):
        tracks = next(os.walk(filedir))[2]
    else:
        print("WARNING: no files directory")
        continue

    uploadsize = 0

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
        uploadsize += track.filesize
        sesh.files.append(track)
        print("----> added {}".format(track.filename))

    if UPLOAD:
        print("Adding session to upload queue...", end=" ", flush=True)
        db.session.add(sesh)
        print("Done ({})".format(AudioFile.readable_filesize(uploadsize)))

        print("Uploading session to database...", end=" ", flush=True)
        try:
            db.session.commit()
            successful_uploads += 1
            print("Done")
        except sqlalchemy.exc.IntegrityError as e:
            print("Aborted")
            print("ERROR: {}".format(e.args[0]))

print(separator)

print(
    "{} of {} sessions successfully uploaded".format(
        successful_uploads, len(sessionlist)
    )
)
