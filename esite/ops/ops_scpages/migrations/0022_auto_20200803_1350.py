# Generated by Django 2.2.12 on 2020-08-03 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ops_scpages', '0021_auto_20200803_1337'),
    ]

    operations = [
        migrations.RenameField(
            model_name='opsscpagespage',
            old_name='feed',
            new_name='feed_section',
        ),
        migrations.RenameField(
            model_name='opsscpagespage',
            old_name='history',
            new_name='history_section',
        ),
        migrations.RenameField(
            model_name='opsscpagespage',
            old_name='languages',
            new_name='languages_section',
        ),
    ]
