# Generated by Django 2.2.12 on 2020-08-03 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops_scpages', '0019_auto_20200803_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opsscpagespage',
            name='opensource_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='opsscpagespage',
            name='recruiting_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]