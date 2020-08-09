from django.db import models
from modelcluster.models import ClusterableModel, ParentalManyToManyField, ParentalKey
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel

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
    GraphQLForeignKey,
    GraphQLCollection,
)


class ContributionFeed(ClusterableModel):
    page = ParentalKey(
        "OpsScpagePage", related_name="epfeed", on_delete=models.SET_NULL, null=True
    )
    type = models.CharField(null=True, max_length=255)
    cid = models.CharField(null=True, max_length=255)
    datetime = models.DateTimeField(null=True)
    message = models.CharField(null=True, max_length=255)
    files = ParentalManyToManyField(
        "ContributionFile", related_name="files", null=True, blank=True
    )

    graphql_fields = [
        GraphQLForeignKey("page", content_type="ops_scpages.Contributor"),
        GraphQLString("type"),
        GraphQLString("cid"),
        GraphQLString("datetime"),
        GraphQLString("message"),
        GraphQLCollection(GraphQLForeignKey, "files", "ops_scpages.ContributionFile"),
    ]

    def __str__(self):
        # (commit) cid
        return f"({self.type}) {self.cid}"


class ContributionFile(models.Model):
    feed = ParentalKey(
        "OpsScpagePage", related_name="epfeed2", on_delete=models.SET_NULL, null=True
    )
    insertions = models.IntegerField(null=True)
    deletions = models.IntegerField(null=True)
    path = models.CharField(null=True, max_length=255)
    raw_changes = models.TextField(null=True, max_length=255)

    graphql_fields = [
        GraphQLForeignKey("page", content_type="ops_scpages.Contributor"),
        GraphQLString("insertions"),
        GraphQLString("deletions"),
        GraphQLString("path"),
        GraphQLString("raw_changes"),
    ]

    def __str__(self):
        # /src/test.py (+100/-200)
        return f"{self.path} (+{self.insertions}/-{self.deletions})"


class CodeLanguageStatistic(models.Model):
    name = models.CharField(null=True, max_length=255, default="Unkown")
    color = models.CharField(null=True, max_length=255, default="Unkown")
    insertions = models.IntegerField(null=True, default="Unkown")
    deletions = models.IntegerField(null=True, default="Unkown")

    graphql_fields = [
        GraphQLString("name"),
        GraphQLString("color"),
        GraphQLString("insertions"),
        GraphQLString("deletions"),
    ]


class CodeTransitionStatistic(models.Model):
    insertions = models.IntegerField(null=True, default="Unkown")
    deletions = models.IntegerField(null=True, default="Unkown")
    datetime = models.DateTimeField(null=True)

    graphql_fields = [
        GraphQLString("insertions"),
        GraphQLString("deletions"),
        GraphQLString("datetime"),
    ]


class Contributor(ClusterableModel):
    page = ParentalKey(
        "OpsScpagePage",
        related_name="epcontributor",
        on_delete=models.SET_NULL,
        null=True,
    )
    name = models.CharField(null=True, max_length=255, default="Unkown")
    username = models.CharField(null=True, max_length=255, default="Unkown")
    active = models.BooleanField(default=True)
    avatar = models.ImageField()
    feed = ParentalManyToManyField(
        "ContributionFeed", related_name="contributor_feed", blank=True
    )
    codelanguages = ParentalManyToManyField(
        "CodeLanguageStatistic", related_name="contributor_codelanguages", blank=True
    )
    codetransition = ParentalManyToManyField(
        "CodeTransitionStatistic", related_name="contributor_codetransition", blank=True
    )

    graphql_fields = [
        GraphQLForeignKey("page", content_type="ops_scpages.Contributor"),
        GraphQLString("name"),
        GraphQLString("username"),
        GraphQLBoolean("active"),
        GraphQLImage("avatar"),
        GraphQLCollection(GraphQLForeignKey, "feed", "ops_scpages.ContributionFeed"),
        GraphQLCollection(
            GraphQLForeignKey, "codelanguages", "ops_scpages.CodeLanguageStatistic"
        ),
        GraphQLCollection(
            GraphQLForeignKey, "codetransition", "ops_scpages.CodeTransitionStatistic"
        ),
    ]

    def __str__(self):
        return f"{self.username}"


class Project(ClusterableModel):
    page = ParentalKey(
        "OpsScpagePage",
        related_name="opsprojects",
        on_delete=models.SET_NULL,
        null=True,
    )

    name = models.CharField(null=True, blank=True, max_length=255, default="Unkown")
    url = models.URLField(null=True, blank=True, max_length=255, default="Unkown")
    description = models.TextField(null=True, blank=True, default="Unkown")
    owner_name = models.CharField(
        null=True, blank=True, max_length=255, default="Unkown"
    )
    owner_username = models.CharField(
        null=True, blank=True, max_length=255, default="Unkown"
    )
    owner_email = models.EmailField(null=True, blank=True, default="Unkown")
    contributors = ParentalManyToManyField(
        "Contributor", related_name="project_contributor", blank=True
    )
    feed = ParentalManyToManyField(
        "ContributionFeed", related_name="project_feed", blank=True
    )
    codelanguages = ParentalManyToManyField(
        "CodeLanguageStatistic", related_name="project_codelanguages", blank=True
    )
    codetransition = ParentalManyToManyField(
        "CodeTransitionStatistic", related_name="project_codetransition", blank=True
    )

    graphql_fields = [
        GraphQLForeignKey("page", content_type="ops_scpages.Project"),
        GraphQLString("name"),
        GraphQLString("url"),
        GraphQLString("description"),
        GraphQLString("owner_name"),
        GraphQLString("owner_username"),
        GraphQLString("owner_email"),
        GraphQLCollection(GraphQLForeignKey, "feed", "ops_scpages.ContributionFeed"),
        GraphQLCollection(GraphQLForeignKey, "contributors", "ops_scpages.Contributor"),
        GraphQLCollection(
            GraphQLForeignKey, "codelanguages", "ops_scpages.CodeLanguageStatistic"
        ),
        GraphQLCollection(
            GraphQLForeignKey, "codetransition", "ops_scpages.CodeLanguageStatistic"
        ),
    ]

    # panel = [InlinePanel("transition_project")]


class OpsScpagesPage(Page):
    # Only allow creating HomePages at the root level
    parent_page_types = ["wagtailcore.Page"]


class OpsScpagePage(Page):
    # feed = ParentalKey(
    #     "ContributionFeed", related_name="epfeed", on_delete=models.SET_NULL, null=True
    # )
    from ...utils.edit_handlers import TestPanel

    content_panels = Page.content_panels + [
        # InlinePanel("epfeed", label="Contributions", heading="Contribution Feed"),
        InlinePanel("opsprojects", label="Project", heading="Projects"),
        # TestPanel("opsprojects")
        # InlinePanel("epcontributor", label="Contributor", heading="Contributors"),
    ]

    graphql_fields = [
        # GraphQLForeignKey("opsprojects", "ops_scpages.Project"),
        GraphQLCollection(GraphQLForeignKey, "opsprojects", "ops_scpages.Project"),
        GraphQLCollection(
            GraphQLForeignKey, "epcontributor", "ops_scpages.Contributor"
        ),
        GraphQLCollection(GraphQLForeignKey, "epfeed", "ops_scpages.ContributionFeed"),
    ]

    def generate(self):
        from ...core.services import mongodb

        data = mongodb.get_collection("gitlab").aggregate(
            [
                {"$match": {"company_page_slug": f"{self.slug}"}},
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
        Project.objects.all().delete()
        Contributor.objects.all().delete()
        ContributionFeed.objects.all().delete()
        ContributionFile.objects.all().delete()
        for project in data:
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

                con, created = Contributor.objects.get_or_create(
                    page=self,
                    name=event["committer_name"],
                    username=event["committer_email"],
                )

                try:
                    files = event["asset"]["Log"]["files"]
                    for file in files:
                        cf, created = ContributionFile.objects.get_or_create(
                            insertions=file["insertions"],
                            deletions=file["deletions"],
                            path=file["path"],
                            raw_changes=file["raw_changes"],
                        )

                        c.files.add(cf)

                        cts, created = CodeTransitionStatistic.objects.get_or_create(
                            datetime=c.datetime,
                            insertions=cf.insertions,
                            deletions=cf.deletions,
                        )

                        con.codetransition.add(cts)
                        p.codetransition.add(cts)
                except:
                    pass

                con.feed.add(c)

                p.contributors.add(con)
                p.feed.add(c)

            p.save()

        # a = ContributionFile.objects.all()
        # print(a)
