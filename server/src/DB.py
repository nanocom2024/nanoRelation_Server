from pymongo import MongoClient


class DB:
    def __init__(self):
        # MongoDBに接続
        client = MongoClient("localhost", 27017)
        db = client["db"]
        self.__users = db["users"]
        self.__device_keys = db["device_keys"]
        self.__pre_pairings = db["pre_pairings"]
        self.__pairings = db["pairings"]

    # users
    @property
    def users(self):
        return self.__users

    # device_keys
    @property
    def device_keys(self):
        return self.__device_keys

    # pre_pairings
    @property
    def pre_pairings(self):
        return self.__pre_pairings

    # pairings
    @property
    def pairings(self):
        return self.__pairings
