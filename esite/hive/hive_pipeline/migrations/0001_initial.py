# Generated by Django 2.2.12 on 2020-08-16 16:31

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0045_assign_unlock_grouppagepermission"),
        ("hive_enterprise", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="OpsPipelineFormPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                    ),
                ),
                (
                    "to_address",
                    models.CharField(
                        blank=True,
                        help_text="Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.",
                        max_length=255,
                        verbose_name="to address",
                    ),
                ),
                (
                    "from_address",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="from address"
                    ),
                ),
                (
                    "subject",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="subject"
                    ),
                ),
                ("head", models.CharField(max_length=255, null=True)),
                ("description", models.CharField(max_length=255, null=True)),
            ],
            options={"abstract": False,},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="Pipeline",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("active", models.BooleanField(default=True)),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "enterprise_page",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pipeline_scp_page",
                        to="hive_enterprise.EnterpriseFormPage",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OpsPipelineFormSubmission",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("form_data", models.TextField()),
                (
                    "submit_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="submit time"),
                ),
                (
                    "page",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wagtailcore.Page",
                    ),
                ),
            ],
            options={
                "verbose_name": "form submission",
                "verbose_name_plural": "form submissions",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OpsPipelineFormField",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "label",
                    models.CharField(
                        help_text="The label of the form field",
                        max_length=255,
                        verbose_name="label",
                    ),
                ),
                (
                    "field_type",
                    models.CharField(
                        choices=[
                            ("singleline", "Single line text"),
                            ("multiline", "Multi-line text"),
                            ("email", "Email"),
                            ("number", "Number"),
                            ("url", "URL"),
                            ("checkbox", "Checkbox"),
                            ("checkboxes", "Checkboxes"),
                            ("dropdown", "Drop down"),
                            ("multiselect", "Multiple select"),
                            ("radio", "Radio buttons"),
                            ("date", "Date"),
                            ("datetime", "Date/time"),
                            ("hidden", "Hidden field"),
                        ],
                        max_length=16,
                        verbose_name="field type",
                    ),
                ),
                (
                    "required",
                    models.BooleanField(default=True, verbose_name="required"),
                ),
                (
                    "choices",
                    models.TextField(
                        blank=True,
                        help_text="Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.",
                        verbose_name="choices",
                    ),
                ),
                (
                    "default_value",
                    models.CharField(
                        blank=True,
                        help_text="Default value. Comma separated values supported for checkboxes.",
                        max_length=255,
                        verbose_name="default value",
                    ),
                ),
                (
                    "help_text",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="help text"
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="form_fields",
                        to="hive_pipeline.OpsPipelineFormPage",
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
        ),
    ]