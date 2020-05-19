from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

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
        # TODO: basepath would be different when executing from server
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

                if sesh.challenge.description is not "":
                    mdpath = os.path.join(seshdir, "challenge.md")
                    zipfile.writestr(mdpath, sesh.challenge.description)

                filedirs = {"files": ""}

                for file in sesh.files:
                    if file.session_subsection:
                        dirname = "files_{}".format(slugify(file.session_subsection))
                        filedirs[dirname] = file.session_subsection
                        savepath = os.path.join(seshdir, dirname, file.filename,)
                    else:
                        savepath = os.path.join(seshdir, "files", file.filename)
                    zipfile.write(file.filepath, savepath)

                sessioninfo = {
                    "session.date": seshdate,
                    "challenge.name": sesh.challenge.name,
                    "challenge.blurb": sesh.challenge.blurb,
                    "session.copyright": sesh.copyright_issues,
                    "filedirs": filedirs,
                }
                jsonpath = os.path.join(seshdir, "sessioninfo.json")
                zipfile.writestr(jsonpath, json.dumps(sessioninfo, indent=4))

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
