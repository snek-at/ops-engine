# Generated by Django 2.2.12 on 2020-09-17 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hive_enterprise', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gitlab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.URLField(max_length=255, null=True)),
                ('token', models.CharField(help_text='Warning! Changing the token affects the connection to all endpoints.', max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('privileges_mode', models.CharField(choices=[('POLP', 'Principle of least privilege'), ('IDC', 'Open privilege')], default='ISOLATE', max_length=255)),
                ('enterprise_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gitlab_scp_page', to='hive_enterprise.EnterpriseFormPage')),
            ],
        ),
    ]
