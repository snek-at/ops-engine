# Generated by Django 2.2.12 on 2020-09-21 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hive_pipeline', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opspipelineformpage',
            name='description',
            field=models.CharField(default='The sumbission form for SITP', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='opspipelineformpage',
            name='head',
            field=models.CharField(default='Pipeline Form', max_length=255, null=True),
        ),
    ]
