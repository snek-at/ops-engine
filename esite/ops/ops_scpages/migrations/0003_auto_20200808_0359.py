# Generated by Django 2.2.12 on 2020-08-08 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops_scpages', '0002_auto_20200808_0337'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='maintainer_email',
            new_name='owner_email',
        ),
        migrations.AddField(
            model_name='contributionfeed',
            name='cid',
            field=models.CharField(max_length=255, null=True),
        ),
    ]