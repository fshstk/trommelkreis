# Generated by Django 3.0.8 on 2021-04-12 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0006_auto_20210405_2300_squashed_0007_remove_audiofile_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofile',
            name='artist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tracks', to='archive.Artist'),
        ),
    ]