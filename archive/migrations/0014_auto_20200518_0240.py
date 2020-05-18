# Generated by Django 3.0.6 on 2020-05-18 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0013_uploadformvars_session_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='audiofile',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='blurb',
            field=models.TextField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
