from django.db import models
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from wagtail.core.models import Page
from wagtail.core import fields
from wagtail.core import blocks
from wagtail.documents import blocks as docblocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.admin.edit_handlers import (
    StreamFieldPanel,
    FieldPanel,
    PageChooserPanel,
    TabbedInterface,
    ObjectList,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey

import uuid
import json
from esite.bifrost.models import (
    GraphQLInt,
    GraphQLBoolean,
    GraphQLString,
    GraphQLFloat,
    GraphQLImage,
    GraphQLDocument,
    GraphQLSnippet,
    GraphQLEmbed,
    GraphQLStreamfield,
)
from esite.bifrost.helpers import register_streamfield_block

# > Sections


class Gitlab(models.Model):
    from ..ops_scpages.models import OpsScpagePage

    name = models.CharField(null=True, max_length=255)
    description = models.CharField(null=True, blank=True, max_length=255)
    url = models.URLField(null=True, max_length=255)
    token = models.CharField(
        null=True,
        max_length=255,
        help_text="Warning! Changing the token affects the connection to all endpoints.",
    )
    created = models.DateTimeField(null=True, auto_now_add=True)
    updated = models.DateTimeField(null=True, auto_now=True)
    active = models.BooleanField(default=True)
    company_page = models.ForeignKey(
        OpsScpagePage,
        on_delete=models.CASCADE,
        related_name="gitlab_scp_page",
        null=True,
        blank=True,
    )

    privilegies_mode = models.CharField(
        choices=[("polp", "Principle of least privilege"), ("idc", "Open privilege"),],
        default="isolate",
        max_length=255,
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("description"),
                FieldPanel("url"),
                FieldPanel("token"),
                FieldPanel("company_page"),
            ],
            heading="General",
        ),
        MultiFieldPanel([FieldPanel("privilegies_mode"),], heading="Settings",),
    ]

    def analyse_gitlab(self):
        from ...core.services import mongodb
        from .services import GitLabScraper

        print(self.url, self.token)
        gls = GitLabScraper(self.token)

        # > Get all projects where token user is member of
        projects = []

        for _projects in gls.gen_request(
            f"{self.url}/projects", optional_parameter="membership=true"
        ):
            # print(_projects)
            # > Get all members of each project
            for project in _projects:
                print("PROJECT", project)
                project["members"] = []
                project["events"] = []

                project_link = project["_links"]["self"]
                member_link = project["_links"]["members"]

                if member_link:
                    for _members in gls.gen_request(member_link):
                        project["members"] += _members

                for _events in gls.gen_request(f"{project_link}/repository/commits"):
                    project["events"] += _events

                project["languages"] = next(
                    gls.gen_request(f"{project_link}/languages")
                )
                projects.append(project)

        # enter the data here
        if self.company_page:
            mongodb.get_collection("gitlab").update(
                {"gitlab_id": self.id},
                {
                    "company_page_slug": f"{self.company_page.slug}",
                    "gitlab_id": self.id,
                    "projects": projects,
                },
                upsert=True,
            )

    def __str__(self):
        return f"{self.name} ({self.url})"


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
