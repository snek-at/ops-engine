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

from .models import Connector

# Create your registration related graphql schemes here.


class ConnectorType(DjangoObjectType):
    class Meta:
        model = Connector
        exclude_fields = []


class AddConnector(graphene.Mutation):
    connector = graphene.Field(ConnectorType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        domain = graphene.String(required=True)
        connector_token = graphene.String(required=True)
        company_page_slug = graphene.String(required=True)
        active = graphene.Boolean(required=True)
        privilegies_mode = graphene.String(required=True)
        share_mode = graphene.String(required=True)
        settings = GenericScalar()

    @superuser_required
    def mutate(
        self,
        info,
        name,
        description,
        domain,
        connector_token,
        company_page_slug,
        active,
        privilegies_mode,
        share_mode,
        settings,
    ):
        from ..ops_scpages.models import OpsScpagePage

        page = OpsScpagePage.objects.get(slug=company_page_slug)

        connector = Connector(
            name=name,
            description=description,
            domain=domain,
            token=connector_token,
            company_page=page,
            privilegies_mode=privilegies_mode,
            share_mode=share_mode,
            **settings,
        )

        connector.save()

        return AddConnector(connector=connector)


class UpdateConnector(graphene.Mutation):
    connector = graphene.Field(ConnectorType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=False)
        description = graphene.String(required=True)
        domain = graphene.String(required=False)
        connector_token = graphene.String(required=False)
        company_page_slug = graphene.String(required=False)
        active = graphene.Boolean(required=False)
        privilegies_mode = graphene.String(required=False)
        share_mode = graphene.String(required=False)
        settings = GenericScalar()

    @superuser_required
    def mutate(self, info, id, company_page_slug, settings, **kwargs):
        from ..ops_scpages.models import OpsScpagePage

        page = OpsScpagePage.objects.filter(slug=company_page_slug).first()

        if page:
            kwargs["company_page"] = page
        else:
            if company_page_slug:
                kwargs["company_page"] = None

        if kwargs["connector_token"]:
            kwargs["token"] = kwargs["connector_token"]
            kwargs.pop("connector_token")

        Connector.objects.filter(id=id).update(**kwargs, **settings)
        connector = Connector.objects.get(id=id)

        return UpdateConnector(connector=connector)


class Mutation(graphene.ObjectType):
    add_connector = AddConnector.Field()
    update_connector = UpdateConnector.Field()


class Query(graphene.ObjectType):
    connectors = graphene.List(ConnectorType)

    @superuser_required
    def resolve_connectors(self, info, **_kwargs):

        return Connector.objects.all()


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
