# Generated by Django 3.0.6 on 2020-05-15 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0003_auto_20200516_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadformvars',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='archive.Session'),
        ),
    ]