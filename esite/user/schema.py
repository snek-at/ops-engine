from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import (
    login_required,
    permission_required,
    staff_member_required,
    superuser_required,
)

from esite.user.models import User

# Create your registration related graphql schemes here.


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude_fields = ["password"]


class Query(graphene.ObjectType):
    me = graphene.Field(UserType, token=graphene.String(required=False))
    users = graphene.List(UserType, token=graphene.String(required=False))

    @login_required
    def resolve_users(self, info, **_kwargs):

        return User.objects.all()

    @login_required
    def resolve_me(self, info, **_kwargs):
        user = info.context.user

        return user


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
