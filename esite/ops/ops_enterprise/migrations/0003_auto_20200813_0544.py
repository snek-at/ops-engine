# Generated by Django 2.2.12 on 2020-08-13 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops_enterprise', '0002_auto_20200812_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enterpriseformpage',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
