# -*- coding: utf-8 -*-
from django.db import migrations
from ...ops.ops_scpages.models import OpsScpagesPage
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

    # Create root page
    # root = Page.objects.create(
    #     title="Root",
    #     slug='root',
    #     content_type=page_content_type,
    #     path='0001',
    #     depth=1,
    #     numchild=1,
    #     url_path='/',
    # )

    # Create homepage
    opsPage = Page.objects.create(
        title="OPS Management",
        slug="ops-management",
        content_type=page_content_type,
        path="00010001",
        depth=2,
        numchild=0,
        url_path="/ops/",
    )

    # page_content_type, created = ContentType.objects.get_or_create(
    #     model="OpsScpagesPage", app_label="ops_scpages"
    # )

    Page.objects.create(
        title="Company Pages",
        slug="company-pages",
        content_type=page_content_type,
        path="000100010001",
        depth=2,
        numchild=0,
        url_path="/company-pages/",
    )

    # Create default site
    Site.objects.create(root_page_id=opsPage.id, is_default_site=True)

    # Site.objects.create(root_page_id=ops2Page.id, is_default_site=False)

    # page_content_type, created = ContentType.objects.get_or_create(
    #     model="OpsScpagesPage", app_label="ops_scpages"
    # )

    # b = Page.objects.create(
    #     title="Company Pages",
    #     slug="company-pages",
    #     content_type=page_content_type,
    #     path="00010002",
    #     depth=2,
    #     numchild=0,
    #     url_path="/cpages/",
    # )
    # Site.objects.create(root_page_id=b.id, is_default_site=False)

    # root = Pagec.objects.get(id=1)
    # root.add_child(instance=b)


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
        ("ops_scpages", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_homepage, remove_homepage),
    ]
