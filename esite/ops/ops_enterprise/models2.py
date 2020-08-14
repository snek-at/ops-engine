import uuid
import json
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.admin.mail import send_mail
from wagtail.core.fields import StreamField, RichTextField
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.edit_handlers import (
    TabbedInterface,
    ObjectList,
    InlinePanel,
    StreamFieldPanel,
    MultiFieldPanel,
    FieldPanel,
)
from wagtail.contrib.forms.models import (
    AbstractEmailForm,
    AbstractFormField,
    AbstractFormSubmission,
)
from wagtail.contrib.forms.models import (
    AbstractForm,
    AbstractFormField,
    AbstractEmailForm,
    AbstractFormSubmission,
)
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from esite.utils.models import BasePage, BaseEmailFormPage
from esite.bifrost.helpers import register_streamfield_block
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
    GraphQLCollection,
    GraphQLForeignKey,
)
from esite.colorfield.blocks import ColorBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core import fields

# Model manager to use in Proxy model
class ProxyManager(BaseUserManager):
    def get_queryset(self):
        # filter the objects for activate enterprise datasets based on the User model
        return super(ProxyManager, self).get_queryset().filter(is_enterprise=True)


class Enterprise(get_user_model()):
    # call the model manager on user objects
    objects = ProxyManager()

    # Panels/fields to fill in the Add enterprise form
    # panels = [
    #     FieldPanel("is_enterprise"),
    #     FieldPanel("date_joined"),
    #     # FieldPanel('title'),
    #     # FieldPanel('first_name'),
    #     # FieldPanel('last_name'),
    #     # FieldPanel('email'),
    #     # FieldPanel('telephone'),
    #     # FieldPanel('address'),
    #     # FieldPanel('zipCode'),
    #     # FieldPanel('city'),
    #     # FieldPanel('country'),
    #     # FieldPanel('newsletter'),
    #     # FieldPanel('cache'),
    # ]

    def __str__(self):
        return self.username

    class Meta:
        proxy = True
        ordering = ("date_joined",)


# > Models
class ContributionFile(ClusterableModel):
    test = models.CharField(null=True, blank=True, max_length=255)


class CodeLanguageStatistic(models.Model):
    test = models.CharField(null=True, blank=True, max_length=255)


class CodeTransitionStatistic(models.Model):
    test = models.CharField(null=True, blank=True, max_length=255)


class ContributionFeed(ClusterableModel):
    test = models.CharField(null=True, blank=True, max_length=255)
    files = ParentalManyToManyField("ContributionFile", related_name="feed_file")

    graphql_fields = [
        GraphQLString("test"),
        GraphQLCollection(
            GraphQLForeignKey, "files", "ops_enterprise.ContributionFile"
        ),
    ]


class ProjectContributor(ClusterableModel):
    project = ParentalKey(
        "Project",
        related_name="project_projectcontributor",
        on_delete=models.SET_NULL,
        null=True,
    )
    feed = ParentalManyToManyField(
        "ContributionFeed", related_name="projectcontributor_feed"
    )

    graphql_fields = [
        GraphQLForeignKey("project", content_type="ops_enterprise.Project"),
        GraphQLCollection(GraphQLForeignKey, "feed", "ops_enterprise.ContributionFeed"),
    ]


class Contributor(ClusterableModel):
    foo = models.CharField(null=True, blank=True, max_length=255)
    feed = ParentalManyToManyField("ContributionFeed", related_name="contributor_feed")

    graphql_fields = [
        GraphQLCollection(GraphQLForeignKey, "feed", "ops_enterprise.ContributionFeed"),
    ]


class Project(ClusterableModel):
    contributors = ParentalManyToManyField(
        "Contributor", related_name="project_contributors"
    )

    graphql_fields = [
        GraphQLCollection(
            GraphQLForeignKey, "contributors", "ops_enterprise.Contributor"
        ),
    ]


class EnterpriseFormPage(Page, ClusterableModel):
    feed = ParentalManyToManyField(
        "ContributionFeed", related_name="page_feed", blank=True
    )
    contributors = ParentalManyToManyField(
        "Contributor", related_name="page_contributors", blank=True
    )
    projects = ParentalManyToManyField(
        "Project", related_name="page_projects", blank=True
    )

    graphql_fields = [
        GraphQLCollection(GraphQLForeignKey, "feed", "ops_enterprise.ContributionFeed"),
        GraphQLCollection(
            GraphQLForeignKey, "contributors", "ops_enterprise.Contributor"
        ),
        GraphQLCollection(GraphQLForeignKey, "projects", "ops_enterprise.Project"),
    ]

    content_panels = Page.content_panels + [FieldPanel("feed")]

    def generate(self):
        from ...core.services import mongodb

        data = mongodb.get_collection("gitlab").aggregate(
            [
                {"$match": {"enterprise_page_slug": f"{self.slug}"}},
                {"$unwind": "$projects"},
                {"$unwind": "$projects.events"},
                {
                    "$lookup": {
                        "from": "pipeline",
                        "let": {"commit_id": "$projects.events.id"},
                        "pipeline": [
                            {"$unwind": "$Log"},
                            {
                                "$match": {
                                    "$expr": {"$eq": ["$$commit_id", "$Log.commit"]},
                                }
                            },
                        ],
                        "as": "projects.events.asset",
                    }
                },
                {
                    "$unwind": {
                        "path": "$projects.events.asset",
                        "preserveNullAndEmptyArrays": True,
                    }
                },
                {
                    "$group": {
                        "_id": "$projects.id",
                        "name": {"$first": "$projects.name"},
                        "url": {"$first": "$projects.http_url_to_repo"},
                        "description": {"$first": "$projects.description"},
                        "maintainer_name": {"$first": "$projects.owner.name"},
                        "maintainer_username": {"$first": "$projects.owner.username"},
                        "maintainer_email": {"$first": "$projects.owner.email"},
                        "events": {"$push": "$projects.events"},
                    }
                },
            ]
        )

        for _project in data:
            project = Project.objects.create()

        # dummy = [{

        # }]

        # if self.slug != "e-sneklab":

        #     project = Project.objects.create()

        #     c = Contributor.objects.create(foo="Test")
        #     feed = ContributionFeed.objects.create(test="abc")
        #     file = ContributionFile.objects.create(test="abc")
        #     feed.files.add(file)
        #     feed.save()
        #     c.feed.add(feed)
        #     c.save()

        #     project.contributors.add(c)
        #     project.save()

        #     self.feed.add(feed)
        #     self.contributors.add(c)
        #     self.projects.add(project)

        #     self.save()


class EnterpriseIndex(BasePage):
    # template = 'patterns/pages/enterprise/person_index_page.html'

    # Only allow creating HomePages at the root level
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["EnterpriseFormPage"]

    class Meta:
        verbose_name = "Enterprise Index"

    def get_context(self, request, *args, **kwargs):
        enterprise = (
            EnterpriseFormPage.objects.live()
            .public()
            .descendant_of(self)
            .order_by("slug")
        )

        page_number = request.GET.get("page", 1)
        paginator = Paginator(enterprise, settings.DEFAULT_PER_PAGE)
        try:
            enterprise = paginator.page(page_number)
        except PageNotAnInteger:
            enterprise = paginator.page(1)
        except EmptyPage:
            enterprise = paginator.page(paginator.num_pages)

        context = super().get_context(request, *args, **kwargs)
        context.update(enterprise=enterprise)

        return context
