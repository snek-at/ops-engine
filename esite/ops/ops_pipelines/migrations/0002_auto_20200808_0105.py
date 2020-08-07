# Generated by Django 2.2.12 on 2020-08-07 23:05

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ops_scpages', '0002_auto_20200808_0105'),
        ('ops_pipelines', '0001_initial'),
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
    ]

    operations = [
        migrations.AddField(
            model_name='pipeline',
            name='company_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pipeline_scp_page', to='ops_scpages.OpsScpagePage'),
        ),
        migrations.AddField(
            model_name='opspipelineformsubmission',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Page'),
        ),
        migrations.AddField(
            model_name='opspipelineformfield',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_fields', to='ops_pipelines.OpsPipelineFormPage'),
        ),
    ]
