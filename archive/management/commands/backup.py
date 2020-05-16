from django.core.management.base import BaseCommand, CommandError

import os
import json
import io
from datetime import datetime
from zipfile import ZipFile

from archive.models import Challenge, Session, Artist, AudioFile


class Command(BaseCommand):
    help = """
    Back up a ZIP archive with archive contents, including database metadata,
    in a format readable by addlocal.py.

    File will be saved to MEDIA_ROOT/trommelkreis-archive-backup-yyyymmdd.zip
    """

    def handle(self, *args, **options):
        basepath = "/Users/fshstk/Downloads"
        archivename = "trommelkreis-archive-backup-{}.zip".format(
            datetime.now().strftime("%Y%m%d")
        )
        archivepath = os.path.join(basepath, archivename)
        if os.path.isfile(archivepath):
            raise CommandError("Error: file {} already exists".format(archivepath))

        archive = io.BytesIO()
        sessionlist = Session.objects.all()
        self.print("Archive name: {}".format(archivename))
        self.print("{} sessions to be backed up".format(len(sessionlist)))

        with ZipFile(archive, "w") as zipfile:
            for sesh in sessionlist:
                seshdate = sesh.date.strftime("%Y%m%d")
                seshdir = sesh.slug
                self.print("Adding session: {}".format(seshdir))

                sessioninfo = {
                    "session.date": seshdate,
                    "challenge.name": sesh.challenge.name,
                    "challenge.blurb": sesh.challenge.blurb,
                    "session.info": sesh.info,
                    "session.copyright": sesh.copyright_issues,
                }
                jsonpath = os.path.join(seshdir, "sessioninfo.json")
                zipfile.writestr(jsonpath, json.dumps(sessioninfo, indent=4))

                if sesh.challenge.description is not "":
                    mdpath = os.path.join(seshdir, "challenge.md")
                    zipfile.writestr(mdpath, sesh.challenge.description)

                for file in sesh.files:
                    savepath = os.path.join(seshdir, "files", file.filename)
                    zipfile.write(file.filepath, savepath)

        archive.seek(0)

        with open(archivepath, "wb") as f:
            self.print("Writing to {}...".format(archivepath))
            f.write(archive.getvalue())

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
