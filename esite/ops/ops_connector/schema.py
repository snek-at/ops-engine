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
        token = graphene.String(required=True)
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        url = graphene.String(required=True)
        connector_token = graphene.String(required=True)
        enterprise_page_slug = graphene.String(required=True)
        active = graphene.Boolean(required=True)
        privileges_mode = graphene.String(required=True)
        share_mode = graphene.String(required=True)
        settings = GenericScalar()

    @superuser_required
    def mutate(
        self,
        info,
        token,
        name,
        description,
        url,
        connector_token,
        enterprise_page_slug,
        active,
        privileges_mode,
        share_mode,
        settings,
    ):
        from ..ops_enterprise.models import EnterpriseFormPage

        page = EnterpriseFormPage.objects.get(slug=enterprise_page_slug)

        connector = Connector(
            name=name,
            description=description,
            url=url,
            token=connector_token,
            enterprise_page=page,
            privileges_mode=privileges_mode,
            share_mode=share_mode,
            **settings,
        )

        connector.save()

        return AddConnector(connector=connector)


class UpdateConnector(graphene.Mutation):
    connector = graphene.Field(ConnectorType)

    class Arguments:
        token = graphene.String(required=True)
        id = graphene.Int(required=True)
        name = graphene.String(required=False)
        description = graphene.String(required=True)
        url = graphene.String(required=False)
        connector_token = graphene.String(required=False)
        enterprise_page_slug = graphene.String(required=False)
        active = graphene.Boolean(required=False)
        privileges_mode = graphene.String(required=False)
        share_mode = graphene.String(required=False)
        settings = GenericScalar(required=False)

    @superuser_required
    def mutate(self, info, token, id, enterprise_page_slug=None, settings={}, **kwargs):
        from ..ops_enterprise.models import EnterpriseFormPage

        page = EnterpriseFormPage.objects.filter(slug=enterprise_page_slug).first()

        if page:
            kwargs["enterprise_page"] = page
        else:
            if enterprise_page_slug:
                kwargs["enterprise_page"] = None

        if kwargs.get("connector_token"):
            kwargs["token"] = kwargs["connector_token"]
            kwargs.pop("connector_token")

        Connector.objects.filter(id=id).update(**kwargs, **settings)
        connector = Connector.objects.get(id=id)

        return UpdateConnector(connector=connector)


class Mutation(graphene.ObjectType):
    add_connector = AddConnector.Field()
    update_connector = UpdateConnector.Field()


class Query(graphene.ObjectType):
    connectors = graphene.List(ConnectorType, token=graphene.String(required=True))

    @superuser_required
    def resolve_connectors(self, info, **_kwargs):

        return Connector.objects.all()


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
