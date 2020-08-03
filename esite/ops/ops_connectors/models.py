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
import secrets

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


class Connector(models.Model):
    from ..ops_scpages.models import OpsScpagesPage

    name = models.CharField(null=True, max_length=255)
    domain = models.CharField(null=True, max_length=255)
    token = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="Warning! Changing the token affects the connection to all endpoints.",
    )
    company_page = ParentalKey(
        OpsScpagesPage,
        on_delete=models.CASCADE,
        related_name="conntector_scp_page",
        null=True,
        blank=True,
    )

    # Settings
    privilegies_mode = models.CharField(
        choices=[("polp", "Principle of least privilege"), ("idc", "Open privilege"),],
        default="isolate",
        max_length=255,
    )
    share_mode = models.CharField(
        choices=[
            (
                "isolate",
                "Prohibit external authentication - Prohibit company page publishing",
            ),
            (
                "medium",
                "Prohibit external authentication - Allow company page publishing",
            ),
            ("open", "Allow external authentication - Allow company page publishing"),
        ],
        default="isolate",
        max_length=255,
    )
    share_projects = models.BooleanField(default=True)
    share_users = models.BooleanField(default=True)
    share_company_name = models.BooleanField(default=True)
    share_company_recruiting = models.BooleanField(default=True)
    share_company_recruement_url = models.BooleanField(default=True)
    share_company_description = models.BooleanField(default=True)
    share_company_emplyees_count = models.BooleanField(default=True)
    share_company_vat = models.BooleanField(default=True)
    share_company_email = models.BooleanField(default=True)
    share_company_opensource_status = models.BooleanField(default=True)
    share_company_opensource_url = models.BooleanField(default=True)

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
        MultiFieldPanel(
            [
                FieldPanel("privilegies_mode"),
                FieldPanel("share_mode"),
                FieldPanel("share_projects"),
                FieldPanel("share_company_name"),
                FieldPanel("share_company_recruiting"),
                FieldPanel("share_company_recruement_url"),
                FieldPanel("share_company_description"),
                FieldPanel("share_company_emplyees_count"),
                FieldPanel("share_company_vat"),
                FieldPanel("share_company_email"),
                FieldPanel("share_company_opensource_status"),
                FieldPanel("share_company_opensource_url"),
            ],
            heading="Settings",
        ),
    ]

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_hex()

        super(Connector, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.domain})"


# class ConnectorForm(AbstractEmailForm):
#     # Only allow creating HomePages at the root level
#     parent_page_types = ["OpsPipelinesPage"]


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
