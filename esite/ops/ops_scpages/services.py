def updatePages():
    from .models import OpsScpagePage

    for page in OpsScpagePage.objects.all():
        page.generate()

    # tmp = mongodb.get_collection("gitlab").aggregate(
    #     [
    #         {"$match": {"company_page_slug": "sneklab"}},
    #         {"$unwind": "$projects"},
    #         {"$unwind": "$projects.events"},
    #         {
    #             "$lookup": {
    #                 "from": "pipeline",
    #                 "let": {"commit_id": "$projects.events.id"},
    #                 "pipeline": [
    #                     {"$unwind": "$Log"},
    #                     {"$match": {"$expr": {"$eq": ["$$commit_id", "$Log.commit"]},}},
    #                 ],
    #                 "as": "projects.events.asset",
    #             }
    #         },
    #         {
    #             "$unwind": {
    #                 "path": "$projects.events.asset",
    #                 "preserveNullAndEmptyArrays": True,
    #             }
    #         },
    #         {
    #             "$group": {
    #                 "_id": "$projects.id",
    #                 "name": {"$first": "$projects.name"},
    #                 "url": {"$first": "$projects.http_url_to_repo"},
    #                 "description": {"$first": "$projects.description"},
    #                 "maintainer_name": {"$first": "$projects.owner.name"},
    #                 "maintainer_username": {"$first": "$projects.owner.username"},
    #                 "maintainer_email": {"$first": "$projects.owner.email"},
    #                 "events": {"$push": "$projects.events"},
    #             }
    #         },
    #     ]
    # )

    # for i in tmp:
    #     print(i)
    # break

    # with open("data.json", "w") as outfile:
    #     json.dump(data["projects"][0], outfile, cls=DjangoJSONEncoder)

