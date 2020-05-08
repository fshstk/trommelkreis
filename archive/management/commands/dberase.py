from django.core.management.base import BaseCommand, CommandError

from archive.models import Challenge, Session, Artist, AudioFile


class Command(BaseCommand):
    help = "Deletes all database items. Proceed with caution."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING(
                "Delete ENTIRE database? (Challenges, Sesions, AudioFiles, Artists)"
            )
        )
        if input("Enter 'yes' to confirm: ") == "yes":
            self.print("Deleting AudioFiles...")
            AudioFile.objects.all().delete()
            self.print("Deleting Artists...")
            Artist.objects.all().delete()
            self.print("Deleting Sessions...")
            Session.objects.all().delete()
            self.print("Deleting Challenges...")
            Challenge.objects.all().delete()
            self.printsuccess("database cleared (Audio Files remain in media/archive/)")
        else:
            raise CommandError("Delete database not confirmed...")

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
