# Generated by Django 2.2.12 on 2020-08-09 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ops_connector', '0001_initial'),
        ('ops_enterprise', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='connector',
            name='enterprise_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conntector_scp_page', to='ops_enterprise.EnterpriseFormPage'),
        ),
    ]
