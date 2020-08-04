from django.conf import settings
from pymongo import MongoClient


mongodb = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
