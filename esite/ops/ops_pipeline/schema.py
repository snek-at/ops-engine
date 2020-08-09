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

from .models import Pipeline

# Create your registration related graphql schemes here.


class PipelineType(DjangoObjectType):
    class Meta:
        model = Pipeline
        exclude_fields = []


class AddPipeline(graphene.Mutation):
    pipeline = graphene.Field(PipelineType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        active = graphene.Boolean(required=False)
        enterprise_page_slug = graphene.String(required=True)

    @superuser_required
    def mutate(self, info, name, description, active, enterprise_page_slug):
        from ..ops_enterprise.models import EnterpriseFormPage

        page = EnterpriseFormPage.objects.get(slug=enterprise_page_slug)

        pipeline = Pipeline(
            name=name, description=description, active=active, enterprise_page=page
        )

        pipeline.save()

        return AddPipeline(pipeline=pipeline)


class UpdatePipeline(graphene.Mutation):
    pipeline = graphene.Field(PipelineType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=False)
        description = graphene.String(required=False)
        active = graphene.Boolean(required=False)
        enterprise_page_slug = graphene.String(required=False)

    @superuser_required
    def mutate(self, info, id, enterprise_page_slug=None, **kwargs):
        from ..ops_enterprise.models import EnterpriseFormPage

        page = EnterpriseFormPage.objects.filter(slug=enterprise_page_slug).first()

        if page:
            kwargs["enterprise_page"] = page
        else:
            if enterprise_page_slug:
                kwargs["enterprise_page"] = None

        Pipeline.objects.filter(id=id).update(**kwargs)
        pipeline = Pipeline.objects.get(id=id)

        return UpdatePipeline(pipeline=pipeline)


class Mutation(graphene.ObjectType):
    add_pipeline = AddPipeline.Field()
    update_pipeline = UpdatePipeline.Field()


class Query(graphene.ObjectType):
    pipelines = graphene.List(PipelineType)

    @superuser_required
    def resolve_pipelines(self, info, **_kwargs):

        return Pipeline.objects.all()


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
