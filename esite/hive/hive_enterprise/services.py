from django.conf import settings
from guesslang import Guess
from datetime import datetime
import os
import yaml

from ...core.services import mongodb
from .models import (
    EnterpriseFormPage,
    Project,
    ContributionFeed,
    Contributor,
    ProjectContributor,
    ContributionFile,
    CodeLanguageStatistic,
    CodeTransitionStatistic,
)

# Read language definition file for later use
with open(os.path.join(settings.BASE_DIR, "esite/hive/languages.yaml")) as f:
    language_table = yaml.load(f, Loader=yaml.FullLoader)


def generate_from_gitlab_with_pipline_injection(page):
    data = mongodb.get_collection("gitlab").aggregate(
        [
            {"$match": {"enterprise_page_slug": f"{page.slug}"}},
            {"$unwind": "$projects"},
            {"$unwind": "$projects.events"},
            {
                "$lookup": {
                    "from": "pipeline",
                    "let": {"commit_id": "$projects.events.id"},
                    "pipeline": [
                        {"$unwind": "$Log"},
                        {"$match": {"$expr": {"$eq": ["$$commit_id", "$Log.commit"]},}},
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

    for project in data:
        if bool(project):
            p, created = Project.objects.get_or_create(
                page=page,
                name=project["name"],
                url=project["url"],
                description=project["description"],
                owner_name=project["maintainer_name"],
                owner_username=project["maintainer_username"],
                owner_email=project["maintainer_email"],
            )

            for event in project["events"]:
                if bool(event):

                    if "committed_date" in event:
                        date = event["committed_date"]
                    elif "authored_date" in event:
                        date = event["authored_date"]
                    elif "created_date" in event:
                        date = event["created_date"]

                    c, created = ContributionFeed.objects.get_or_create(
                        page=page,
                        type="commit",
                        datetime=date,
                        cid=event["id"],
                        message=event["message"],
                    )

                    (
                        project_contributor,
                        created,
                    ) = ProjectContributor.objects.get_or_create(
                        project=p, username=event["committer_email"],
                    )
                    project_contributor.name = event["committer_name"]

                    contributor, created = Contributor.objects.get_or_create(
                        page=page, username=event["committer_email"],
                    )
                    contributor.name = event["committer_name"]

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

                            # Analyse raw_changes for programming languages
                            language_name = Guess().language_name(file["raw_changes"])
                            langguage_statistic = language_table[language_name]

                            # Check if language_statistic is a subgroup of a main
                            # language, if so take group as new language_statistic
                            if "group" in langguage_statistic:
                                language_name = langguage_statistic["group"]
                                langguage_statistic = language_table[language_name]

                            (
                                code_language_statistic,
                                created,
                            ) = CodeLanguageStatistic.objects.get_or_create(
                                page=page,
                                name=language_name,
                                primary_extension=langguage_statistic[
                                    "primary_extension"
                                ],
                                type=langguage_statistic["type"],
                                color=langguage_statistic["color"]
                                if "color" in langguage_statistic
                                else "#8C92AC",
                            )

                            code_language_statistic.insertions += file["insertions"]
                            code_language_statistic.deletions += file["deletions"]

                            code_language_statistic.save()

                            c.files.add(cf)

                            (
                                cts,
                                created,
                            ) = CodeTransitionStatistic.objects.get_or_create(
                                page=page,
                                datetime=c.datetime,
                                insertions=cf.insertions,
                                deletions=cf.deletions,
                            )

                            c.codelanguages.add(code_language_statistic)
                            project_contributor.codetransition.add(cts)
                            project_contributor.codelanguages.add(
                                code_language_statistic
                            )
                            contributor.codetransition.add(cts)
                            contributor.codelanguages.add(code_language_statistic)
                            p.codelanguages.add(code_language_statistic)
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

                    p.contributors.add(project_contributor)
                    p.contribution_feed.add(c)

            p.save()


def generate_from_pipeline(page):
    data = mongodb.get_collection("pipeline").find(
        {"enterprise_page_slug": f"{page.slug}"}
    )

    for pipeline in data:
        project, created = Project.objects.get_or_create(
            page=page, url=pipeline["repository_url"]
        )
        for log_entry in pipeline["Log"]:
            contribution, created = ContributionFeed.objects.get_or_create(
                page=page,
                type="commit",
                datetime=datetime.strptime(
                    log_entry["date"], "%a %b %d %H:%M:%S %Y %z"
                ),
                cid=log_entry["commit"],
                message=log_entry["message"],
            )

            username, email = log_entry["author"].split(" <")
            email = email.rstrip(">")

            (project_contributor, created,) = ProjectContributor.objects.get_or_create(
                project=project, username=email,
            )
            project_contributor.name = username

            contributor, created = Contributor.objects.get_or_create(
                page=page, username=email,
            )
            contributor.name = username

            for file in log_entry["files"]:
                contribution_file, created = ContributionFile.objects.get_or_create(
                    feed=contribution,
                    insertions=int(file["insertions"]),
                    deletions=int(file["deletions"]),
                    path=file["path"],
                    raw_changes=file["raw_changes"],
                )

                # Analyse raw_changes for programming languages
                language_name = Guess().language_name(file["raw_changes"])
                langguage_statistic = language_table[language_name]

                # Check if language_statistic is a subgroup of a main
                # language, if so take group as new language_statistic
                if "group" in langguage_statistic:
                    language_name = langguage_statistic["group"]
                    langguage_statistic = language_table[language_name]

                (
                    code_language_statistic,
                    created,
                ) = CodeLanguageStatistic.objects.get_or_create(
                    page=page,
                    name=language_name,
                    primary_extension=langguage_statistic["primary_extension"],
                    type=langguage_statistic["type"],
                    color=langguage_statistic["color"]
                    if "color" in langguage_statistic
                    else "#8C92AC",
                )

                code_language_statistic.insertions += int(file["insertions"])
                code_language_statistic.deletions += int(file["deletions"])

                code_language_statistic.save()

                contribution.files.add(contribution_file)

                (
                    code_transition_statistic,
                    created,
                ) = CodeTransitionStatistic.objects.get_or_create(
                    page=page,
                    datetime=contribution.datetime,
                    insertions=contribution_file.insertions,
                    deletions=contribution_file.deletions,
                )

                contribution.codelanguages.add(code_language_statistic)
                project_contributor.codetransition.add(code_transition_statistic)
                project_contributor.codelanguages.add(code_language_statistic)
                contributor.codetransition.add(code_transition_statistic)
                contributor.codelanguages.add(code_language_statistic)
                project.codetransition.add(code_transition_statistic)
                project.codelanguages.add(code_language_statistic)

                contribution.save()
                project_contributor.save()
                contributor.save()
                project.save()

            project_contributor.contribution_feed.add(contribution)
            project_contributor.save()
            contributor.contribution_feed.add(contribution)
            contributor.save()

            project.contributors.add(project_contributor)
            project.contribution_feed.add(contribution)

        project.save()


def updatePages():
    for page in EnterpriseFormPage.objects.all():
        # In theory the generate_from_pipeline would replace the pipeline
        # injection into gitlab because. Someone should take a deep insight in
        # this perfomence issue. Maybe we should use MongoDB for deeper
        # aggregation in the future.
        generate_from_gitlab_with_pipline_injection(page)
        generate_from_pipeline(page)
