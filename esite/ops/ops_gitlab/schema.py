from django.contrib.auth import get_user_model

import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import (
    login_required,
    permission_required,
    staff_member_required,
    superuser_required,
)
import json

from .models import Gitlab

# Create your registration related graphql schemes here.


class GitlabType(DjangoObjectType):
    class Meta:
        model = Gitlab
        exclude_fields = []


class AddGitlab(graphene.Mutation):
    gitlab = graphene.Field(GitlabType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        domain = graphene.String(required=True)
        gitlab_token = graphene.String(required=True)
        enterprise_page_slug = graphene.String(required=True)
        active = graphene.Boolean(required=True)
        privilegies_mode = graphene.String(required=True)

    @superuser_required
    def mutate(
        self,
        info,
        name,
        description,
        domain,
        gitlab_token,
        enterprise_page_slug,
        privilegies_mode,
    ):
        from ..ops_enterprise.models import EnterpriseFormPage

        page = EnterpriseFormPage.objects.get(slug=enterprise_page_slug)

        gitlab = Gitlab(
            name=name,
            description=description,
            domain=domain,
            token=gitlab_token,
            enterprise_page=page,
            privilegies_mode=privilegies_mode,
        )

        gitlab.save()

        return AddGitlab(gitlab=gitlab)


class UpdateGitlab(graphene.Mutation):
    gitlab = graphene.Field(GitlabType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=False)
        description = graphene.String(required=False)
        domain = graphene.String(required=False)
        gitlab_token = graphene.String(required=False)
        enterprise_page_slug = graphene.String(required=False)
        active = graphene.Boolean(required=False)
        privilegies_mode = graphene.String(required=False)

    @superuser_required
    def mutate(self, info, id, enterprise_page_slug=None, **kwargs):
        from ..ops_enterprise.models import EnterpriseFormPage

        page = EnterpriseFormPage.objects.filter(slug=enterprise_page_slug).first()

        if page:
            kwargs["enterprise_page"] = page
        else:
            if enterprise_page_slug:
                kwargs["enterprise_page"] = None

        print(kwargs)

        if kwargs.get("gitlab_token"):
            kwargs["token"] = kwargs.get("gitlab_token")
            kwargs.pop("gitlab_token")

        Gitlab.objects.filter(id=id).update(**kwargs)
        gitlab = Gitlab.objects.get(id=id)

        gitlab.analyse_gitlab()

        return UpdateGitlab(gitlab=gitlab)


class Mutation(graphene.ObjectType):
    add_gitlab = AddGitlab.Field()
    update_gitlab = UpdateGitlab.Field()


class Query(graphene.ObjectType):
    gitlabs = graphene.List(GitlabType)

    @superuser_required
    def resolve_gitlabs(self, info, **_kwargs):

        return Gitlab.objects.all()


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
