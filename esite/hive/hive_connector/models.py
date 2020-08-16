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
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import uuid
import json
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
    enterprise_page = ParentalKey(
        "hive_enterprise.EnterpriseFormPage",
        on_delete=models.CASCADE,
        related_name="connector_scp_page",
        null=True,
        blank=True,
    )

    # Settings
    privileges_mode = models.CharField(
        choices=[("POLP", "Principle of least privilege"), ("IDC", "Open privilege"),],
        default="POLP",
        max_length=255,
    )
    is_hashed = models.BooleanField(default=True)
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
                FieldPanel("is_hashed"),
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

    def publish(self):
        from django.forms.models import model_to_dict

        data_to_publish = {
            "enterprise_imprint": {},
            "enterprise_contributors": {},
            "enterprise_projects": {},
            "enterprise_codelanguage_statistic": {},
            "enterprise_codetransition_statistic": {},
        }

        # Imprint
        data_to_publish["enterprise_imprint"] = {
            "city": self.enterprise_page.city,
            "zip_code": self.enterprise_page.zip_code,
            "address": self.enterprise_page.address,
            "telephone": self.enterprise_page.telephone,
            "telefax": self.enterprise_page.telefax,
            "vat_number": self.enterprise_page.vat_number
            if self.share_company_vat
            else None,
            "whatsapp_telephone": self.enterprise_page.whatsapp_telephone,
            "whatsapp_contactline": self.enterprise_page.whatsapp_contactline,
            "tax_id": self.enterprise_page.tax_id,
            "trade_register_number": self.enterprise_page.trade_register_number,
            "court_of_registry": self.enterprise_page.court_of_registry,
            "place_of_registry": self.enterprise_page.place_of_registry,
            "ownership": self.enterprise_page.ownership,
            "email": self.enterprise_page.email if self.share_company_email else None,
            "employee_count": self.enterprise_page.employee_count
            if self.share_company_employees_count
            else None,
            "opensource_url": self.enterprise_page.opensource_url
            if self.share_company_opensource_url
            else None,
            "recruiting_url": self.enterprise_page.recruiting_url
            if self.share_company_recruement_url
            else None,
            "description": self.enterprise_page.description
            if self.share_company_description
            else None,
        }

        enterprise_contributors = [
            obj.for_publish(self.is_hashed)
            for obj in self.enterprise_page.enterprise_contributors.all()
        ]

        if self.share_users:
            for index, contributor in enumerate(enterprise_contributors):
                enterprise_contributors[index]["codetransition"] = [
                    obj.for_publish(self.is_hashed)
                    for obj in contributor["codetransition"].all()
                ]
                enterprise_contributors[index]["codelanguages"] = [
                    obj.for_publish(self.is_hashed)
                    for obj in contributor["codelanguages"].all()
                ]

            data_to_publish["enterprise_contributors"] = enterprise_contributors

        if self.share_projects:
            enterprise_projects = [
                obj.for_publish(self.is_hashed)
                for obj in self.enterprise_page.enterprise_projects.all()
            ]

            for index, project in enumerate(enterprise_projects):
                enterprise_projects[index]["contributors"] = [
                    obj.for_publish(self.is_hashed)
                    for obj in project["contributors"].all()
                ]
                enterprise_projects[index]["codetransition"] = [
                    obj.for_publish(self.is_hashed)
                    for obj in project["codetransition"].all()
                ]
                enterprise_projects[index]["codelanguages"] = [
                    obj.for_publish(self.is_hashed)
                    for obj in project["codelanguages"].all()
                ]

            data_to_publish["enterprise_projects"] = enterprise_projects

        data_to_publish["enterprise_codetransition_statistic"] = [
            obj.for_publish(self.is_hashed)
            for obj in self.enterprise_page.enterprise_codetransition_statistic.all()
        ]

        data_to_publish["enterprise_codelanguage_statistic"] = [
            obj.for_publish(self.is_hashed)
            for obj in self.enterprise_page.enterprise_codelanguage_statistic.all()
        ]

        """ Send data to enterprise connector """

        transport = RequestsHTTPTransport(
            url=self.url,
            use_json=True,
            headers={"Content-type": "application/json",},
            verify=False,
            retries=3,
        )

        client = Client(transport=transport, fetch_schema_from_transport=True,)

        params = {
            "page": json.dumps(data_to_publish),
            "token": self.token,
            "enterpriseName": self.enterprise_page.title,
        }

        # Auth
        query = gql(
            """
            mutation ($page: JSONString!, $token: String!, $enterpriseName: String!) {
                publishCompanyPage(page: $page, token: $token, enterpriseName: $enterpriseName) {
                    result {
                    __typename
                    }
                }
            }
        """
        )

        print(params)

        res = client.execute(query, variable_values=json.dumps(params))


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

        # Connector.objects.get


class ConnectorFormSubmission(AbstractFormSubmission):
    pass


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2020 Simon Prast
