from flask import Blueprint, request, jsonify
from settings import Settings
from os.path import join, dirname
from DB import DB
from firebase_admin import auth
from Auth import firebase
from Child.ChildrenModel import add_child


CHILD_BP = Blueprint('child', __name__, url_prefix='/child')

# Settings インスタンス
settings = Settings(join(dirname(__file__), '../../.env'))

# MongoDBに接続
db = DB()
users = db.users


@CHILD_BP.route('/register_child', methods=['POST'])
def register_child():
    # parentのtoken
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400
    # childのemail
    email = request.json['email']
    if not email:
        return jsonify({'error': 'Missing email'}), 400
    # childのpassword
    password = request.json['password']
    if not password:
        return jsonify({'error': 'Missing password'}), 400

    # tokenの認証(parent)
    parent = users.find_one({'token': token})
    if not parent:
        return jsonify({'error': 'Invalid token'}), 400

    if parent['email'] == email:
        return jsonify({'error': 'can not register own'}), 400

    # ユーザーの認証(child)
    try:
        auth.get_user_by_email(email)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # パスワードの認証(child)
    firebase_api_key = settings.firebase_api_key
    res = firebase.sign_in_with_email_and_password(
        firebase_api_key, email, password)

    if 'error' in res:
        return jsonify({'error': res['error']['message']}), 400

    if not users.find({'email': email}):
        # firebaseにuserが存在するが、DBには存在しない場合
        return jsonify({'error': 'User not found'}), 400
    else:
        users.update_one({'email': email}, {'$set': {'token': res['idToken']}})

    child = users.find_one({'email': email})
    add_child(parent_uid=parent['uid'], child_uid=child['uid'])

    return jsonify({'done': 'register'}), 200
