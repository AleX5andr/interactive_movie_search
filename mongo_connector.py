import pymongo.errors
import settings as se
import user_interface as ui
import sys
from pymongo import MongoClient
from pymongo.synchronous.collection import Collection
from datetime import datetime
from logger import log_error


@log_error()
def client_open() -> tuple[MongoClient, Collection]:
    """
    Connects to MongoDB and returns the client and target collection.

    :return: A tuple (MongoClient, Collection) for database access.

    Exits if the connection fails.
    """
    client = MongoClient(se.MONGO_URL)
    coll = client["ich_edit"][se.MONGO_COLLECTION]
    return client, coll


@log_error()
def add_request(choice: str | list, quantity: int) -> None:
    """
    Saves a search request to MongoDB with timestamp and result count.

    :param choice: Search input; either a keyword (str) or a list.
    :param quantity: Number of results returned by the search.

    :raises SystemExit: If database insertion fails.
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
        ui.error_print(pymongo.errors.WriteError("Error adding document to MongoDB."))
        sys.exit(0)
    client.close()


@log_error()
def get_queries(choice: str) -> tuple:
    """
    Retrieves either the 5 most recent or 5 most frequent search queries from MongoDB.

    :param choice: Type of query selection.
    :return: A tuple of formatted search query records.

    :raises SystemExit: If the MongoDB connection fails internally.
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
