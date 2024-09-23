from pymongo import MongoClient


class DB:
    def __init__(self):
        # MongoDBに接続
        client = MongoClient("localhost", 27017)
        db = client["db"]
        self.__users = db["users"]
        self.__device_keys = db["device_keys"]
        self.__pairings = db["pairings"]
        self.__pre_passes = db["pre_passes"]
        self.__now_passes = db["now_passes"]
        self.__log_passes = db["log_passes"]
        self.__notification_config = db["notification_config"]
        self.__children = db["children"]
        self.__lost_children = db["lost_children"]
        self.__log_lost_children = db["log_lost_children"]
        self.__log_own = db["log_own"]
        self.__log_lost_passes = db["log_lost_passes"]
        self.__log_near_own_children = db["log_near_own_children"]

    # users
    @property
    def users(self):
        return self.__users

    # device_keys
    @property
    def device_keys(self):
        return self.__device_keys

    # pairings
    @property
    def pairings(self):
        return self.__pairings

    # pre_passes
    @property
    def pre_passes(self):
        return self.__pre_passes

    # now_passes
    @property
    def now_passes(self):
        return self.__now_passes

    # log_passes
    @property
    def log_passes(self):
        return self.__log_passes

    # notification_config
    @property
    def notification_config(self):
        return self.__notification_config

    # children
    @property
    def children(self):
        return self.__children

    # lost_children
    @property
    def lost_children(self):
        return self.__lost_children

    # log_lost_children
    @property
    def log_lost_children(self):
        return self.__log_lost_children

    # log_own
    @property
    def log_own(self):
        return self.__log_own

    # log_lost_passes
    @property
    def log_lost_passes(self):
        return self.__log_lost_passes

    # log_near_own_children
    @property
    def log_near_own_children(self):
        return self.__log_near_own_children
