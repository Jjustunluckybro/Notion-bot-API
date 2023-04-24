import pymongo
from datetime import datetime
from config import MONGO_TEST_DB_CONNECTION_PATH


class MongoAPI:

    def __init__(self):
        self._connect_to_db()

    def _connect_to_db(self):
        self._client = pymongo.MongoClient(MONGO_TEST_DB_CONNECTION_PATH)
        self._db = self._client.Notes
        self._collection = self._db.notes

    def insert_one_to_collection(self, obj: dict) -> None:
        _id = obj["_id"]
        self._collection.insert_one(obj)

    def get_by_id(self, _id: int, is_show_id: bool = False) -> tuple:
        return self._collection.find_one({"_id": _id}, {"_id": int(is_show_id)})

    def get_all_by_name(self, name: str, is_show_id: bool = False) -> tuple:
        return tuple(self._collection.find({"name": name}, {"_id": int(is_show_id)}))

    def get_all_by_description_regex(self, regex_exp: str, is_show_is: bool = False) -> tuple():
        # regex = {"$regex": regex_exp}
        query = {"description": {"$regex": regex_exp}}
        return tuple(self._collection.find(query, {"_id": int(is_show_is)}))


if __name__ == '__main__':
    db = MongoAPI()

    data = {
        "_id": 1,
        "name": "Name",
        "description": "Some text",
        "create_time": datetime.now()
    }
    # print(db.get_all_by_name("Name"))
    # print(db.get_by_id(1))
    # print(db.get_all_by_description_regex("S*"))