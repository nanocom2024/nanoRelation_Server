from pymongo import MongoClient

# MongoDBに接続
client = MongoClient("localhost", 27017)

db = client["db"]
users = db["users"]

# ユーザー一覧を取得
for user in users.find():
    print(user)
