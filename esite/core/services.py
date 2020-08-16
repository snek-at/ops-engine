from django.conf import settings
from pymongo import MongoClient

mongoclient = MongoClient(
    f"mongodb+srv://"
    f"{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}"
    f"/?retryWrites=true&w=majority"
)

mongodb = mongoclient.get_database("ops_analytics")

# if not "ops_analytics" in mongoclient.list_database_names():

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
