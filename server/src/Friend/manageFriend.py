from pymongo import MongoClient

from DB import DB

db = DB()

users = db.users
friends = db.friends

def integrity():
    # usersDBから全ユーザーのuidを取得
    uids = []
    for user in users.find():
        uids.append(user["uid"])

    # friendsDBにuidを追加
    for uid in uids:
        # friendsDBにuidが存在しない場合、uidを追加
        if not friends.find_one({"uid": uid}):
            print("uid not found in friendsDB" + uid)
            friends.insert_one({"uid": uid, "friends": []})

    # userDBに存在しないuidを削除
    for friend in friends.find():
        if friend["uid"] not in uids:
            print("uid not found in usersDB" + friend["uid"])
            friends.delete_one({"uid": friend["uid"]})


def add_friend(uid, friend_uid):
    # uidが存在しない場合、エラー
    if not friends.find_one({"uid": uid}):
        if users.find_one({"uid": uid}): integrity()
        else:
            print("uid not found")
            return False
    # フレンドがすでに存在する場合、エラー
    if friends.find_one({"uid": uid, "friends": friend_uid}):
        print("friend already exists")
        return False

    # フレンドのuidを追加
    friends.update_one( {"uid": uid}, {"$push": {"friends": friend_uid}} )

def remove_friend(uid, friend_uid):
    # uidが存在しない場合、エラー
    if not friends.find_one({"uid": uid}):
        print("uid not found")
        return False
    # フレンドが存在しない場合、エラー
    if not friends.find_one({"uid": uid, "friends": friend_uid}):
        print("friend not found")
        return False

    # フレンドのuidを削除
    friends.update_one( {"uid": uid}, {"$pull": {"friends": friend_uid}} )

def get_friends(uid):
    # uidが存在しない場合、エラー
    if not friends.find_one({"uid": uid}):
        print("uid not found")
        return False

    # フレンドのuidを取得
    return friends.find_one({"uid": uid})["friends"]
