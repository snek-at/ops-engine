# Generated by Django 2.2.12 on 2020-08-01 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='bigintegerfield',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='booleanfield',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='charfield',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='datefield',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='datetimefield',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='decimalfield',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='durationfield',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='emailfield',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='floatfield',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='genericipaddressfield',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='imagefield',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='integerfield',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='nullbooleanfield',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='positiveintegerfield',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='positivesmallintegerfield',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='sections',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='slugfield',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='smallintegerfield',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='textfield',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='timefield',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='urlfield',
        ),
        migrations.RemoveField(
            model_name='opsdashbordpage',
            name='uuidfield',
        ),
        migrations.AddField(
            model_name='opsdashbordpage',
            name='intro',
            field=models.CharField(default='', max_length=255),
        ),
    ]
