from DB import DB
import random
import string


# MongoDBに接続
db = DB()


def create_account(uid: str, name: str, email: str, token: str) -> dict:
    """
    ユーザーアカウントを作成する(DBに追加)

    :param str uid:
    :param str name:
    :param str email:
    :param str token:
    :return user: dict
    """
    name_id = genarate_username_id(name)
    user = {
        'uid': uid,
        'name': name,
        'name_id': name_id,
        'email': email,
        'token': token
    }
    db.users.insert_one(user)
    return user


def genarate_username_id(name: str) -> str:
    """
    ユーザー名のIDを生成する

    これにより、同じ名前のユーザーが複数いても区別できる

    :param str name:
    :return: 四桁のID (例: ab3d)
    """
    id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    id = '#' + id
    if db.users.find_one({'name': name, 'name_id': id}):
        return genarate_username_id(name)

    return id
