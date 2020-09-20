from django.conf import settings
from pymongo import MongoClient

# mongoclient = MongoClient(
#     f"mongodb+srv://"
#     f"{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}"
#     f"/?retryWrites=true&w=majority"
# )

mongoclient = MongoClient(
    settings.MONGO_HOST,
    username=settings.MONGO_USER,
    password=settings.MONGO_PASSWORD,
)

mongodb = mongoclient.get_database("ops_analytics")

# if not "hive_analytics" in mongoclient.list_database_names():

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
