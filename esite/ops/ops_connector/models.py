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
    FieldRowPanel,
)
from wagtail.admin.mail import send_mail
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
from wagtail.contrib.forms.models import (
    AbstractForm,
    AbstractFormField,
    AbstractEmailForm,
    AbstractFormField,
    AbstractFormSubmission,
)
from esite.bifrost.helpers import register_streamfield_block


class Connector(models.Model):
    name = models.CharField(null=True, max_length=255)
    description = models.CharField(null=True, blank=True, max_length=255)
    url = models.URLField(null=True, max_length=255)
    token = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="Warning! Changing the token affects the connection to all endpoints.",
    )
    created = models.DateTimeField(null=True, auto_now_add=True)
    updated = models.DateTimeField(null=True, auto_now=True)
    active = models.BooleanField(default=True)
    enterprise_page = models.ForeignKey(
        "ops_enterprise.EnterpriseFormPage",
        on_delete=models.CASCADE,
        related_name="conntector_scp_page",
        null=True,
        blank=True,
    )

    # Settings
    privileges_mode = models.CharField(
        choices=[("POLP", "Principle of least privilege"), ("IDC", "Open privilege"),],
        default="POLP",
        max_length=255,
    )
    share_mode = models.CharField(
        choices=[
            (
                "ISOLATE",
                "Prohibit external authentication - Prohibit company page publishing",
            ),
            (
                "MEDIUM",
                "Prohibit external authentication - Allow company page publishing",
            ),
            ("OPEN", "Allow external authentication - Allow company page publishing"),
        ],
        default="ISOLATE",
        max_length=255,
    )
    share_projects = models.BooleanField(default=True)
    share_users = models.BooleanField(default=True)
    share_company_name = models.BooleanField(default=True)
    share_company_recruiting = models.BooleanField(default=True)
    share_company_recruement_url = models.BooleanField(default=True)
    share_company_description = models.BooleanField(default=True)
    share_company_employees_count = models.BooleanField(default=True)
    share_company_vat = models.BooleanField(default=True)
    share_company_email = models.BooleanField(default=True)
    share_company_opensource_status = models.BooleanField(default=True)
    share_company_opensource_url = models.BooleanField(default=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("description"),
                FieldPanel("url"),
                FieldPanel("token"),
                FieldPanel("enterprise_page"),
            ],
            heading="General",
        ),
        MultiFieldPanel(
            [
                FieldPanel("privileges_mode"),
                FieldPanel("share_mode"),
                FieldPanel("share_projects"),
                FieldPanel("share_users"),
                FieldPanel("share_company_name"),
                FieldPanel("share_company_recruiting"),
                FieldPanel("share_company_recruement_url"),
                FieldPanel("share_company_description"),
                FieldPanel("share_company_employees_count"),
                FieldPanel("share_company_vat"),
                FieldPanel("share_company_email"),
                FieldPanel("share_company_opensource_status"),
                FieldPanel("share_company_opensource_url"),
            ],
            heading="Settings",
        ),
    ]

    def __str__(self):
        return f"{self.name} ({self.url})"


class ConnectorFormField(AbstractFormField):
    page = ParentalKey(
        "ConnectorFormPage",
        on_delete=models.CASCADE,
        related_name="form_fields",
        null=True,
    )


class ConnectorFormPage(AbstractEmailForm):
    # Only allow creating HomePages at the root level
    parent_page_types = ["wagtailcore.Page"]

    # When creating a new Form page in Wagtail
    head = models.CharField(null=True, blank=False, max_length=255)
    description = models.CharField(null=True, blank=False, max_length=255)

    graphql_fields = [
        GraphQLString("head"),
        GraphQLString("description"),
    ]

    content_panels = AbstractEmailForm.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("head", classname="full title"),
                FieldPanel("description", classname="full"),
            ],
            heading="content",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            heading="Email Settings",
        ),
        MultiFieldPanel(
            [InlinePanel("form_fields", label="Form fields")], heading="data",
        ),
    ]

    def get_submission_class(self):
        return ConnectorFormSubmission

    # Called when pipeline data is pushed
    def send_mail(self, form):
        addresses = [x.strip() for x in self.to_address.split(",")]

        emailheader = "New SNEK Connector Activity"

        content = []
        for field in form:
            value = field.value()
            if isinstance(value, list):
                value = ", ".join(value)
            content.append("{}: {}".format(field.label, value))
        content = "\n".join(content)

        content += "\n\nMade with ❤ by a tiny SNEK"

        # emailfooter = '<style>@keyframes pulse { 10% { color: red; } }</style><p>Made with <span style="width: 20px; height: 1em; color:#dd0000; animation: pulse 1s infinite;">&#x2764;</span> by <a style="color: lightgrey" href="https://www.aichner-christian.com" target="_blank">Werbeagentur Christian Aichner</a></p>'

        # html_message = f"{emailheader}\n\n{content}\n\n{emailfooter}"

        send_mail(
            self.subject, f"{emailheader}\n\n{content}", addresses, self.from_address
        )

    def process_form_submission(self, form):

        git = (form.cleaned_data["git"],)
        log = (form.cleaned_data["log"],)

        print("PROCESSING")
        print(git, log)
        # Connector.objects.get


class ConnectorFormSubmission(AbstractFormSubmission):
    pass


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
