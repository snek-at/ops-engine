# Generated by Django 2.2.12 on 2020-08-03 20:51

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ops_gitlabs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gitlab',
            name='company_page',
            field=modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gitlab_scp_page', to='ops_scpages.OpsScpagesPage'),
        ),
    ]