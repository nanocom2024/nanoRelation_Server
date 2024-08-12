from pymongo import MongoClient

# MongoDBに接続
client = MongoClient("localhost", 27017)

# データベース一覧を取得
dbs = client.list_database_names()
print(dbs)

db = input('which database do you want to see collections?\n')
collections = client[db].list_collection_names()
print(collections)
