# Generated by Django 3.0.6 on 2020-05-16 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0011_audiofile_session'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='info',
        ),
    ]