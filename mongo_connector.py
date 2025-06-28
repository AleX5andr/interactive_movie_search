import settings as se
import sys
from pymongo import MongoClient
from pymongo.synchronous.collection import Collection
from datetime import datetime


def client_open() -> tuple[MongoClient, Collection]:
    """

    """
    try:
        client = MongoClient(se.MONGO_URL)
        if not client.admin.command("ping"):
            raise ConnectionError("Connection failed.")
        coll = client["ich_edit"][se.MONGO_COLLECTION]
    except ConnectionError as error:
        print(error)
        sys.exit(0)
    else:
        return client, coll


def add_request(choice: str | list, quantity: int) -> None:
    """

    """
    client, coll = client_open()
    now = datetime.now()
    if isinstance(choice, str):
        search_choice = "Keyword"
        params = {"keyword": choice}
    else:
        search_choice = "Genre and year"
        params = {"genre": choice[0]}
        if isinstance(choice[1], int):
            params["year"] = choice[1]
        elif isinstance(choice[1], list):
            params["start_year"] = choice[1][0]
            params["end_year"] = choice[1][1]
        else:
            params["year"] = None
    item = {
        "timestamp": now,
        "search_type": search_choice,
        "params": params,
        "results_count": quantity
    }
    result = coll.insert_one(item)
    if not result.acknowledged:
        print("Error adding document to MongoDB.")
        sys.exit(0)
    client.close()


def get_queries(choice: str) -> tuple:
    """

    """
    client, coll = client_open()
    if choice == "recent":
        data = coll.find({}, {"_id": 0}).sort("timestamp", -1).limit(5)
    else:
        data = coll.aggregate([
            {"$group": {
                "_id": "$params",
                "count": {"$sum": 1},
                "search_type": {"$first": "$search_type"},
                "results_count": {"$first": "$results_count"}
            }},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ])
        # print(*data, sep="\n")
        # time.sleep(3)
    result = []
    for item in data:
        if choice == "recent":
            column_1 = item.get("timestamp").strftime("%Y-%m-%d %H:%M:%S") if item.get("timestamp") else ""
            params = [p for p in item.get("params", {}).values()]
        else:
            column_1 = item.get("count")
            params = [p for p in item.get("_id", {}).values()]
        if len(params) > 1:
            column_3 = f"Genre - '{params[0]}'"
            if len(params) == 3:
                column_3 += f", years '{params[1]} - {params[2]}'"
            if len(params) == 2:
                if params[1]:
                    column_3 += f", year '{params[1]}'"
        else:
            column_3 = f"Keyword - '{str(*params)}'"
        values = [
            column_1,
            item.get("search_type"),
            column_3,
            item.get("results_count")
        ]
        result.append(tuple(values))
    data = tuple(result)
    client.close()
    return data
