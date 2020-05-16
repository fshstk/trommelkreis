from django.core.management.base import BaseCommand, CommandError
from django.core.files import File as DjangoFile
from django.db.utils import IntegrityError

import os
import json
from datetime import datetime
from mutagen.mp3 import EasyMP3

from archive.models import Challenge, Session, Artist, AudioFile


class Command(BaseCommand):
    help = """
    Add files from local directory to database.
    All added files/sessions/challenges must not already be in the database,
    or unpredicted behaviour will occur.
    
    Usage:
    ./manage.py addlocal /full/path/to/archive/

    Directory structure must be as follows:
    archive/
        <sessions: yyyymmdd>/
            sessioninfo.json
            challenge.md
            files/
                <files.mp3>

    sessioninfo.json must include the following keys:
        "session.date" (yyyymmdd, must be identical to directory name)
        "challenge.name"
        "session.info" (optional)
        "challenge.blurb" (optional but recommended)

    challenge.md is an optional markdown document containing long-form challenge
    info (saved to challenge.description); may contain HTML/JS.
    """

    def add_arguments(self, parser):
        parser.add_argument("archive_path")

    def handle(self, *args, **options):
        archive_path = options["archive_path"]
        sessionlist = next(os.walk(archive_path))[1]
        sessionlist.sort()

        for dirname in sessionlist:
            self.print("--------------------------------------------")
            self.print("Directory: {}".format(dirname))

            seshpath = os.path.join(archive_path, dirname)
            markdownfile = os.path.join(seshpath, "challenge.md")
            infofile = os.path.join(seshpath, "sessioninfo.json")
            filedir = os.path.join(seshpath, "files")

            try:
                with open(infofile) as f:
                    seshinfo = json.load(f)
            except FileNotFoundError:
                self.printerror("missing sessioninfo.json")
                continue
            except json.decoder.JSONDecodeError:
                self.printerror("malformed or unreadable sessioninfo.json")
                continue

            try:
                copyflag = seshinfo["copyright"]
            except KeyError:
                self.printwarning("missing copyright flag. Assuming False.")
                copyflag = False

            try:
                date_from_json = seshinfo["session.date"]
            except KeyError:
                self.printerror("missing date in sessioninfo.json")
                continue

            try:
                (challenge, challengecreated) = Challenge.objects.get_or_create(
                    name=seshinfo["challenge.name"], copyright_issues=copyflag
                )
            except KeyError:
                self.printerror("missing challenge.name in sessioninfo.json")
                continue
            if challengecreated:
                self.printsuccess("created challenge: {}".format(challenge.name))
            else:
                self.print("Challenge: {}".format(challenge.name))

            try:
                (sesh, sessioncreated) = Session.objects.get_or_create(
                    date=datetime.strptime(dirname, "%Y%m%d"), challenge=challenge,
                )
            except ValueError:
                self.printerror("directory name needs to be <yyyymmdd>")
                continue
            if sessioncreated:
                self.printsuccess("created session: {}".format(sesh.date))
            else:
                self.printnotice("session already exists")

            if dirname != date_from_json:
                self.printerror("mismatch between directory name and sessioninfo.json")
                continue

            if os.path.isdir(filedir):
                tracks = next(os.walk(filedir))[2]
            else:
                self.printerror("no files directory")
                continue

            try:
                sesh.challenge.blurb = seshinfo["challenge.blurb"]
            except KeyError:
                self.printwarning("missing challenge.blurb")

            try:
                with open(markdownfile) as f:
                    sesh.challenge.markdown = f.read()
            except FileNotFoundError:
                self.printnotice("missing challenge.md")

            sesh.challenge.save()
            sesh.save()

            for filename in tracks:
                if not filename.endswith(".mp3"):
                    self.printnotice("unallowed file suffix: {}".format(filename))
                    continue

                filepath = os.path.join(filedir, filename)

                mp3 = EasyMP3(filepath)
                if mp3.info.sketchy:
                    self.printerror("invalid mp3 file: {}".format(filename))
                    continue

                if "title" in mp3:
                    trackname = mp3["title"][0]
                else:
                    # Strip off .mp3 suffix:
                    trackname = os.path.splitext(filename)[0]

                track = AudioFile(session=sesh, name=trackname)
                try:
                    track.save()
                except IntegrityError:
                    self.printwarning("file {} already exists".format(filename))
                    continue

                with DjangoFile(open(filepath, "rb")) as f:
                    savepath = os.path.join(dirname, filename)
                    track.data.save(savepath, f)
                    self.printsuccess("added {}".format(trackname))

                if "artist" in mp3:
                    (track.artist, artistcreated) = Artist.objects.get_or_create(
                        name=mp3["artist"][0]
                    )
                    track.save()
                    if artistcreated:
                        self.printsuccess("created artist: {}".format(track.artist))

    # TODO: move these to separate file... _printfunctions.py?
    def printerror(self, msg):
        self.stdout.write(self.style.ERROR("ERROR: {}".format(str(msg))))

    def printnotice(self, msg):
        self.stdout.write(self.style.NOTICE("NOTICE: {}".format(str(msg))))

    def printsuccess(self, msg):
        self.stdout.write(self.style.SUCCESS("SUCCESS: {}".format(str(msg))))

    def printwarning(self, msg):
        self.stdout.write(self.style.WARNING("WARNING: {}".format(str(msg))))

    def print(self, msg):
        self.stdout.write(str(msg))
