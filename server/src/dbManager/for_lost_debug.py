from pymongo import MongoClient

# MongoDBに接続
client = MongoClient("localhost", 27017)

db = client["db"]
lost_children = db["lost_children"]

# config
major = "1"
minor = "1"


def insert_lost_child():
    lost_child = {
        'major': major,
        'minor': minor
    }
    res = lost_children.insert_one(lost_child)
    if not res:
        print("Failed to insert lost child")
        exit(1)


def delete_lost_child():
    lost_child = {
        'major': major,
        'minor': minor
    }
    res = lost_children.delete_one(lost_child)
    if not res:
        print("Failed to delete lost child")
        exit(1)


if __name__ == "__main__":
    insert_lost_child()
    # delete_lost_child()
