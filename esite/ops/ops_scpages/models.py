from django.db import models
from modelcluster.models import ClusterableModel, ParentalManyToManyField, ParentalKey
from wagtail.core.models import Page


class ContributionFeed(ClusterableModel):
    type = models.CharField(null=True, max_length=255)
    datetime = models.DateTimeField(null=True, max_length=255)
    message = models.CharField(null=True, max_length=255)
    files = ParentalManyToManyField("ContributionFile", related_name="files")


class ContributionFile(models.Model):
    insertions = models.CharField(null=True, max_length=255)
    deletions = models.CharField(null=True, max_length=255)
    path = models.CharField(null=True, max_length=255)
    raw_changes = models.TextField(null=True, max_length=255)


class OpsScpagesPage(Page):
    # Only allow creating HomePages at the root level
    parent_page_types = ["wagtailcore.Page"]


class OpsScpagePage(Page):
    feed = ParentalKey(
        "ContributionFeed", related_name="epfeed", on_delete=models.CASCADE
    )

