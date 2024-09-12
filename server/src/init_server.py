from firebase_admin import auth
from DB import DB

db = DB()
users = db.users


def db_init():
    # ユーザーがDBに存在して，Firebaseに存在しない場合はDBから削除
    firebase_users = auth.list_users()
    db_users = users.find()

    firebase_uids = [user.uid for user in firebase_users.users]

    for db_user in db_users:
        if db_user['uid'] not in firebase_uids:
            users.delete_one({'uid': db_user['uid']})
