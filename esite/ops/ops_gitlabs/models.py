from django.db import models
from django.conf import settings
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
    from ..ops_scpages.models import OpsScpagesPage

    name = models.CharField(null=True, max_length=255)
    domain = models.CharField(null=True, max_length=255)
    token = models.CharField(
        null=True,
        max_length=255,
        help_text="Warning! Changing the token affects the connection to all endpoints.",
    )
    company_page = ParentalKey(
        OpsScpagesPage,
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
                FieldPanel("domain"),
                FieldPanel("token"),
                FieldPanel("company_page"),
            ],
            heading="General",
        ),
        MultiFieldPanel([FieldPanel("privilegies_mode"),], heading="Settings",),
    ]

    def __str__(self):
        return f"{self.name} ({self.domain})"


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
