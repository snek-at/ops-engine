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
from django.contrib.auth import authenticate, login
import json

from .models import OpsScpagePage

# Create your registration related graphql schemes here.


class EnterprisePageType(DjangoObjectType):
    class Meta:
        model = OpsScpagePage
        exclude_fields = []


class PublishEnterprisePage(graphene.Mutation):
    enterprise_page = graphene.Field(EnterprisePageType)

    class Arguments:
        token = graphene.String(required=False)
        company_page_slug = graphene.String(required=True)
        password = graphene.String(required=True)

    @superuser_required
    def mutate(self, info, company_page_slug, password, **kwargs):
        user = authenticate(
            info.context, username=info.context.user.username, password=password
        )

        page = OpsScpagePage.objects.filter(slug=company_page_slug).first()
        
        if page:
            
        return PublishEnterprisePage(enterprise_page=enterprise_page)


class Mutation(graphene.ObjectType):
    add_pipeline = AddPipeline.Field()
    update_pipeline = UpdatePipeline.Field()


class Query(graphene.ObjectType):
    pipelines = graphene.List(PipelineType)

    @login_required
    def resolve_pipelines(self, info, **_kwargs):

        return Pipeline.objects.all()


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
