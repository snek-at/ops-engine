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
class ContributionFeed(ClusterableModel):
    page = ParentalKey(
        "EnterpriseFormPage",
        related_name="enterprise_contribution_feed",
        on_delete=models.SET_NULL,
        null=True,
    )
    type = models.CharField(null=True, max_length=255)
    cid = models.CharField(null=True, max_length=255)
    datetime = models.DateTimeField(null=True)
    message = models.CharField(null=True, max_length=255)
    files = ParentalManyToManyField(
        "ContributionFile", related_name="files", null=True, blank=True
    )

    graphql_fields = [
        GraphQLForeignKey("page", content_type="ops_enterprise.Contributor"),
        GraphQLString("type"),
        GraphQLString("cid"),
        GraphQLString("datetime"),
        GraphQLString("message"),
        GraphQLCollection(
            GraphQLForeignKey, "files", "ops_enterprise.ContributionFile"
        ),
    ]

    def __str__(self):
        # (commit) cid
        return f"({self.type}) {self.cid}"


class ContributionFile(models.Model):
    feed = ParentalKey(
        "ContributionFeed",
        related_name="file_contribution_feed",
        on_delete=models.SET_NULL,
        null=True,
    )
    insertions = models.IntegerField(null=True)
    deletions = models.IntegerField(null=True)
    path = models.CharField(null=True, max_length=255)
    raw_changes = models.TextField(null=True, max_length=255)

    graphql_fields = [
        GraphQLString("insertions"),
        GraphQLString("deletions"),
        GraphQLString("path"),
        GraphQLString("raw_changes"),
    ]

    def __str__(self):
        # /src/test.py (+100/-200)
        return f"{self.path} (+{self.insertions}/-{self.deletions})"


class CodeLanguageStatistic(models.Model):
    page = ParentalKey(
        "EnterpriseFormPage",
        related_name="enterprise_codelanguage_statistic",
        on_delete=models.SET_NULL,
        null=True,
    )
    name = models.CharField(null=True, max_length=255, default="Unkown")
    color = models.CharField(null=True, max_length=255, default="Unkown")
    insertions = models.IntegerField(null=True, default=0)
    deletions = models.IntegerField(null=True, default=0)

    graphql_fields = [
        GraphQLString("name"),
        GraphQLString("color"),
        GraphQLString("insertions"),
        GraphQLString("deletions"),
    ]


class CodeTransitionStatistic(models.Model):
    page = ParentalKey(
        "EnterpriseFormPage",
        related_name="enterprise_codetransition_statistic",
        on_delete=models.SET_NULL,
        null=True,
    )

    insertions = models.IntegerField(null=True, default=0)
    deletions = models.IntegerField(null=True, default=0)
    datetime = models.DateTimeField(null=True)

    graphql_fields = [
        GraphQLString("insertions"),
        GraphQLString("deletions"),
        GraphQLString("datetime"),
    ]


class Contributor(ClusterableModel):
    page = ParentalKey(
        "EnterpriseFormPage",
        related_name="enterprise_contributors",
        on_delete=models.SET_NULL,
        null=True,
    )
    name = models.CharField(null=True, max_length=255, default="Unkown")
    username = models.CharField(null=True, max_length=255, default="Unkown")
    active = models.BooleanField(default=True)
    avatar = models.ImageField(null=True)
    contribution_feed = ParentalManyToManyField(
        "ContributionFeed", related_name="contributor_feed", blank=True
    )
    codelanguages = ParentalManyToManyField(
        "CodeLanguageStatistic", related_name="contributor_codelanguages", blank=True,
    )
    codetransition = ParentalManyToManyField(
        "CodeTransitionStatistic",
        related_name="contributor_codetransition",
        blank=True,
    )

    graphql_fields = [
        GraphQLForeignKey("page", content_type="ops_enterprise.EnterpriseFormPage"),
        GraphQLString("name"),
        GraphQLString("username"),
        GraphQLBoolean("active"),
        GraphQLImage("avatar"),
        GraphQLCollection(
            GraphQLForeignKey, "contribution_feed", "ops_enterprise.ContributionFeed"
        ),
        GraphQLCollection(
            GraphQLForeignKey, "codelanguages", "ops_enterprise.CodeLanguageStatistic"
        ),
        GraphQLCollection(
            GraphQLForeignKey,
            "codetransition",
            "ops_enterprise.CodeTransitionStatistic",
        ),
    ]

    def __str__(self):
        return f"{self.username}"


class ProjectContributor(ClusterableModel):
    project = ParentalKey(
        "Project",
        related_name="project_projectcontributor",
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(null=True, max_length=255, default="Unkown")
    username = models.CharField(null=True, max_length=255, default="Unkown")
    active = models.BooleanField(default=True)
    avatar = models.ImageField(null=True)
    contribution_feed = ParentalManyToManyField(
        "ContributionFeed", related_name="projectcontributor_feed", blank=True
    )
    codelanguages = ParentalManyToManyField(
        "CodeLanguageStatistic",
        related_name="projectcontributor_codelanguages",
        blank=True,
    )
    codetransition = ParentalManyToManyField(
        "CodeTransitionStatistic",
        related_name="projectcontributor_codetransition",
        blank=True,
    )

    graphql_fields = [
        GraphQLForeignKey("project", content_type="ops_enterprise.ProjectContributor"),
        GraphQLString("name"),
        GraphQLString("username"),
        GraphQLBoolean("active"),
        GraphQLImage("avatar"),
        GraphQLCollection(
            GraphQLForeignKey, "contribution_feed", "ops_enterprise.ContributionFeed"
        ),
        GraphQLCollection(
            GraphQLForeignKey, "codelanguages", "ops_enterprise.CodeLanguageStatistic"
        ),
        GraphQLCollection(
            GraphQLForeignKey,
            "codetransition",
            "ops_enterprise.CodeTransitionStatistic",
        ),
    ]

    def __str__(self):
        return f"{self.username}"


class Project(ClusterableModel):
    page = ParentalKey(
        "EnterpriseFormPage",
        related_name="enterprise_projects",
        on_delete=models.SET_NULL,
        null=True,
    )

    name = models.CharField(null=True, blank=True, max_length=255, default="Unkown")
    url = models.URLField(
        null=True, blank=True, max_length=255, default="https://example.local"
    )
    description = models.TextField(null=True, blank=True, default="Unkown")
    owner_name = models.CharField(
        null=True, blank=True, max_length=255, default="Unkown"
    )
    owner_username = models.CharField(
        null=True, blank=True, max_length=255, default="Unkown"
    )
    owner_email = models.EmailField(null=True, blank=True, default="test@snek.at")
    contributors = ParentalManyToManyField(
        "ProjectContributor", related_name="project_contributor", blank=True
    )
    contribution_feed = ParentalManyToManyField(
        "ContributionFeed", related_name="project_feed", blank=True
    )
    codelanguages = ParentalManyToManyField(
        "CodeLanguageStatistic", related_name="project_codelanguages", blank=True
    )
    codetransition = ParentalManyToManyField(
        "CodeTransitionStatistic", related_name="project_codetransition", blank=True
    )

    graphql_fields = [
        GraphQLForeignKey("page", content_type="ops_enterprise.Project"),
        GraphQLString("name"),
        GraphQLString("url"),
        GraphQLString("description"),
        GraphQLString("owner_name"),
        GraphQLString("owner_username"),
        GraphQLString("owner_email"),
        GraphQLCollection(
            GraphQLForeignKey, "contribution_feed", "ops_enterprise.ContributionFeed"
        ),
        GraphQLCollection(
            GraphQLForeignKey, "contributors", "ops_enterprise.ProjectContributor"
        ),
        GraphQLCollection(
            GraphQLForeignKey, "codelanguages", "ops_enterprise.CodeLanguageStatistic"
        ),
        GraphQLCollection(
            GraphQLForeignKey,
            "codetransition",
            "ops_enterprise.CodeTransitionStatistic",
        ),
    ]


# > Pages
class EnterpriseFormField(AbstractFormField):
    page = ParentalKey(
        "EnterpriseFormPage", on_delete=models.CASCADE, related_name="form_fields"
    )


class EnterpriseFormSubmission(AbstractFormSubmission):
    pass


class EnterpriseFormPage(BaseEmailFormPage):
    # Only allow creating HomePages at the root level
    parent_page_types = ["EnterpriseIndex"]
    subpage_types = []
    graphql_fields = []

    class Meta:
        verbose_name = "Enterprise Form Page"

    """[Tabs]
    Wagtail content and API definition of all tabs
    """
    # Overview
    overview_panel = []
    graphql_fields = [
        # GraphQLForeignKey("enterprise_projects", "ops_enterprise.Project"),
        GraphQLCollection(
            GraphQLForeignKey, "enterprise_projects", "ops_enterprise.Project"
        ),
        GraphQLCollection(
            GraphQLForeignKey, "enterprise_contributors", "ops_enterprise.Contributor"
        ),
        GraphQLCollection(
            GraphQLForeignKey,
            "enterprise_contribution_feed",
            "ops_enterprise.ContributionFeed",
        ),
        GraphQLCollection(
            GraphQLForeignKey,
            "enterprise_codetransition_statistic",
            "ops_enterprise.CodeTransitionStatistic",
        ),
        GraphQLCollection(
            GraphQLForeignKey,
            "enterprise_codelanguage_statistic",
            "ops_enterprise.CodeLanguageStatistic",
        ),
    ]
    # Users

    # Imprint
    imprint_tab_name = models.CharField(null=True, blank=True, max_length=255)
    city = models.CharField(null=True, blank=True, max_length=255)
    zip_code = models.CharField(null=True, blank=True, max_length=255)
    address = models.CharField(null=True, blank=True, max_length=255)
    telephone = models.CharField(null=True, blank=True, max_length=255)
    telefax = models.CharField(null=True, blank=True, max_length=255)
    vat_number = models.CharField(null=True, blank=True, max_length=255)
    whatsapp_telephone = models.CharField(null=True, blank=True, max_length=255)
    whatsapp_contactline = models.CharField(null=True, blank=True, max_length=255)
    tax_id = models.CharField(null=True, blank=True, max_length=255)
    trade_register_number = models.CharField(null=True, blank=True, max_length=255)
    court_of_registry = models.CharField(null=True, blank=True, max_length=255)
    place_of_registry = models.CharField(null=True, blank=True, max_length=255)
    ownership = models.CharField(null=True, blank=True, max_length=255)
    email = models.EmailField(null=True, blank=True)
    employee_count = models.CharField(null=True, blank=True, max_length=255)
    opensource_url = models.URLField(null=True, blank=True)
    recruiting_url = models.URLField(null=True, blank=True)
    description = models.CharField(null=True, blank=True, max_length=255)

    imprint_panels = [
        FieldPanel("imprint_tab_name"),
        MultiFieldPanel(
            [
                FieldPanel("city"),
                FieldPanel("zip_code"),
                FieldPanel("address"),
                FieldPanel("telephone"),
                FieldPanel("telefax"),
                FieldPanel("whatsapp_telephone"),
                FieldPanel("whatsapp_contactline"),
                FieldPanel("email"),
            ],
            heading="contact",
        ),
        MultiFieldPanel(
            [
                FieldPanel("vat_number"),
                FieldPanel("tax_id"),
                FieldPanel("court_of_registry"),
                FieldPanel("place_of_registry"),
                FieldPanel("trade_register_number"),
                FieldPanel("ownership"),
            ],
            heading="legal",
        ),
        MultiFieldPanel(
            [
                FieldPanel("employee_count"),
                FieldPanel("opensource_url"),
                FieldPanel("recruiting_url"),
                FieldPanel("description"),
            ],
            heading="about",
        ),
    ]

    graphql_fields += [
        GraphQLString("imprint_tab_name"),
        GraphQLString("city"),
        GraphQLString("zip_code"),
        GraphQLString("address"),
        GraphQLString("telephone"),
        GraphQLString("telefax"),
        GraphQLString("vat_number"),
        GraphQLString("whatsapp_telephone"),
        GraphQLString("whatsapp_contactline"),
        GraphQLString("tax_id"),
        GraphQLString("trade_register_number"),
        GraphQLString("court_of_registry"),
        GraphQLString("place_of_registry"),
        GraphQLString("ownership"),
        GraphQLString("email"),
        GraphQLString("employee_count"),
        GraphQLString("opensource_url"),
        GraphQLString("recruiting_url"),
        GraphQLString("description"),
    ]
    # Settings
    settings_tab_name = models.CharField(null=True, blank=True, max_length=255)
    cache = models.TextField(null=True, blank=True)

    cache_panels = [FieldPanel("cache")]
    form_panels = [
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

    graphql_fields += [
        GraphQLString("cache"),
    ]

    edit_handler = TabbedInterface(
        [
            # ObjectList(Page.content_panels + overview_panels, heading="Overview"),
            ObjectList(Page.content_panels, heading="Overview"),
            # ObjectList(user_panels, heading="Users"),
            # ObjectList(project_panels, heading="Projects"),
            ObjectList(imprint_panels, heading="Imprint"),
            ObjectList(form_panels, heading="Form"),
            ObjectList(
                BasePage.promote_panels + BasePage.settings_panels + cache_panels,
                heading="Settings",
                classname="settings",
            ),
        ]
    )

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
        # print(data)
        Project.objects.all().delete()
        Contributor.objects.all().delete()
        ContributionFeed.objects.all().delete()
        CodeLanguageStatistic.objects.all().delete()
        CodeTransitionStatistic.objects.all().delete()
        ContributionFile.objects.all().delete()

        for project in data:
            # print(project)
            p, created = Project.objects.get_or_create(
                page=self,
                name=project["name"],
                url=project["url"],
                description=project["description"],
                owner_name=project["maintainer_name"],
                owner_username=project["maintainer_username"],
                owner_email=project["maintainer_email"],
            )

            for event in project["events"]:
                c, created = ContributionFeed.objects.get_or_create(
                    page=self,
                    type="commit",
                    datetime=event["created_at"],
                    cid=event["id"],
                    message=event["message"],
                )

                print("pp", p.name)

                project_contributor, created = ProjectContributor.objects.get_or_create(
                    project=p,
                    name=event["committer_name"],
                    username=event["committer_email"],
                )

                contributor, created = Contributor.objects.get_or_create(
                    page=self,
                    name=event["committer_name"],
                    username=event["committer_email"],
                )

                try:
                    files = event["asset"]["Log"]["files"]
                    for file in files:
                        cf, created = ContributionFile.objects.get_or_create(
                            feed=c,
                            insertions=file["insertions"],
                            deletions=file["deletions"],
                            path=file["path"],
                            raw_changes=file["raw_changes"],
                        )

                        c.files.add(cf)

                        # print(c.files.all())

                        cts, created = CodeTransitionStatistic.objects.get_or_create(
                            page=self,
                            datetime=c.datetime,
                            insertions=cf.insertions,
                            deletions=cf.deletions,
                        )

                        project_contributor.codetransition.add(cts)
                        contributor.codetransition.add(cts)
                        p.codetransition.add(cts)

                        c.save()
                        project_contributor.save()
                        contributor.save()
                        p.save()
                except Exception as ex:
                    pass

                project_contributor.contribution_feed.add(c)
                project_contributor.save()
                contributor.contribution_feed.add(c)
                contributor.save()
                # print(project_contributor.name, c.cid)

                p.contributors.add(project_contributor)
                p.contribution_feed.add(c)

            p.save()
        print(Contributor.objects.all()[0].page)
        # print(
        #     p.name,
        #     p.contributors.filter(
        #         username="florian.kleber@edu.htl-villach.at"
        #     ).codetransition,
        # )

    def get_submission_class(self):
        return EnterpriseFormSubmission

    # Create a new user
    def create_enterprise_user(
        self, cache,
    ):
        # enter the data here
        user = get_user_model()(
            username="anexia", is_enterprise=True, is_active=False, cache=cache,
        )

        user.set_password("password")

        user.save()

        return user

    # Called when a user registers
    def send_mail(self, form):
        addresses = [x.strip() for x in self.to_address.split(",")]

        emailheader = "New registration via Pharmaziegasse Website"

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
        print(form.cleaned_data)
        EnterpriseFormPage.objects.filter(id=self.id).update(**form.cleaned_data)

        self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder), page=self,
        )

        if self.to_address:
            self.send_mail(form)


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
