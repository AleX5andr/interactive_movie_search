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
