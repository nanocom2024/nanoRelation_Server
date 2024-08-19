from pymongo import MongoClient

# MongoDBに接続
client = MongoClient("localhost", 27017)

# dbを削除
client.drop_database("db")
