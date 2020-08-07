import json
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
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)
import ast
import uuid
import secrets
from datetime import datetime
from wagtail.admin.mail import send_mail
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
from wagtail.contrib.forms.models import (
    AbstractForm,
    AbstractFormField,
    AbstractEmailForm,
    AbstractFormField,
    AbstractFormSubmission,
)
from esite.utils.edit_handlers import ReadOnlyPanel


class PipelineActivity(models.Model):
    datetime = models.DateTimeField(null=True)
    # data = models.Da
    pipeline = models.ForeignKey("Pipeline", on_delete=models.CASCADE)


class Pipeline(models.Model):
    from ..ops_scpages.models import OpsScpagePage

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(null=True, blank=True, max_length=255)
    description = models.CharField(null=True, blank=True, max_length=255)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(null=True, auto_now_add=True)
    updated = models.DateTimeField(null=True, auto_now=True)
    company_page = models.ForeignKey(
        OpsScpagePage,
        on_delete=models.CASCADE,
        related_name="pipeline_scp_page",
        null=True,
        blank=True,
    )

    panels = [
        MultiFieldPanel(
            [
                ReadOnlyPanel("id", heading="Token"),
                FieldPanel("name"),
                FieldPanel("description"),
                FieldPanel("active"),
                FieldPanel("token"),
                FieldPanel("company_page"),
            ],
            heading="General",
        ),
    ]

    def analyse(self, raw_data: dict):
        from ...core.services import mongodb

        if "Git" in raw_data:
            return Exception("Key: `Git` not valid")

        mongodb.get_collection("pipeline").update(
            {"pipeline_id": self.id},
            {
                "$addToSet": {"Log": {"$each": raw_data["Git"]}},
                "company_page_slug": f"{self.company_page.slug}",
            },
            upsert=True,
        )

    def __str__(self):
        # latest_activity = PipelineActivity.objects.filter(pipeline=self).last()
        return f"{self.name}"


# Form
class OpsPipelineFormField(AbstractFormField):
    page = ParentalKey(
        "OpsPipelineFormPage", on_delete=models.CASCADE, related_name="form_fields",
    )


class OpsPipelineFormPage(AbstractEmailForm):
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
        return OpsPipelineFormSubmission

    # Create a new user
    def handle_input(
        self, id, raw_data,
    ):
        Pipeline.objects.get(id=id).analyse(raw_data=raw_data)

    # Called when pipeline data is pushed
    def send_mail(self, form):
        addresses = [x.strip() for x in self.to_address.split(",")]

        emailheader = "New SNEK OPS Pipeline"

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
        self.handle_input(raw_data=ast.literal_eval(form.cleaned_data["raw_data"]))

        self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder), page=self,
        )

        if self.to_address:
            self.send_mail(form)


class OpsPipelineFormSubmission(AbstractFormSubmission):
    pass
    # user = models.ForeignKey(OpsPipelinesPage, on_delete=models.CASCADE)


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
