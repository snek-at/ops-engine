# -*- coding: utf-8 -*-
from django.db import migrations
from ...hive.hive_enterprise.models import EnterpriseIndex
from wagtail.core.models import Page as Pagec


def create_homepage(apps, schema_editor):
    # Get models
    ContentType = apps.get_model("contenttypes.ContentType")
    Page = apps.get_model("wagtailcore.Page")
    Site = apps.get_model("wagtailcore.Site")

    # Delete the default homepage
    # If migration is run multiple times, it may have already been deleted
    Page.objects.filter(id=2).delete()

    # Create page content type
    page_content_type, created = ContentType.objects.get_or_create(
        model="page", app_label="wagtailcore"
    )

    # Create homepage
    enterprise_page = Page.objects.create(
        title="OPS Management",
        slug="ops-management",
        content_type=page_content_type,
        path="00010001",
        depth=2,
        numchild=0,
        url_path="/ops/",
    )

    # Create default site
    Site.objects.create(root_page_id=enterprise_page.id, is_default_site=True)


def remove_homepage(apps, schema_editor):
    # Get models
    ContentType = apps.get_model("contenttypes.ContentType")
    OpsPageModel = apps.get_model("home.HomePage")

    # Delete the default homepage
    # Page and Site objects CASCADE
    OpsPageModel.objects.filter(slug="opsmanagement", depth=2).delete()

    # Delete content type for homepage model ???
    ContentType.objects.filter(model="homepage", app_label="home").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("hive_enterprise", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_homepage, remove_homepage),
    ]
