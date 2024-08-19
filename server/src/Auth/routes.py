from flask import Blueprint, request, jsonify
from settings import Settings
from os.path import join, dirname
from DB import DB
from firebase_admin import auth
from flask_jwt_extended import create_access_token
from Auth import firebase

AUTH_BP = Blueprint('auth', __name__, url_prefix='/auth')

# Settings インスタンス
settings = Settings(join(dirname(__file__), '../../.env'))

# MongoDBに接続
db = DB()
users = db.users
device_keys = db.device_keys
pre_pairings = db.pre_pairings
pairings = db.pairings


@AUTH_BP.route('/signup', methods=['POST'])
def signup():
    name = request.json['name']
    if not name:
        return jsonify({'error': 'Missing name'}), 400
    email = request.json['email']
    if not email:
        return jsonify({'error': 'Missing email'}), 400
    password = request.json['password']
    if not password:
        return jsonify({'error': 'Missing password'}), 400

    try:
        user = auth.create_user(email=email, password=password)
        access_token = create_access_token(identity=user.uid)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    if users.find_one({'email': email}):
        users.delete_many({'email': email})

    user = {
        'uid': user.uid,
        'name': name,
        'email': email,
        'token': access_token
    }
    res = users.insert_one(user)

    if not res:
        return jsonify({'error': 'Failed to insert user'}), 400

    return jsonify({'token': access_token}), 200


@AUTH_BP.route('/signin', methods=['POST'])
def signin():
    email = request.json['email']
    if not email:
        return jsonify({'error': 'Missing email'}), 400
    password = request.json['password']
    if not password:
        return jsonify({'error': 'Missing password'}), 400

    # ユーザーの認証
    try:
        auth.get_user_by_email(email)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # パスワードの認証
    firebase_api_key = settings.firebase_api_key
    res = firebase.sign_in_with_email_and_password(
        firebase_api_key, email, password)

    if 'error' in res:
        return jsonify({'error': res['error']['message']}), 400

    users.update_one({'email': email}, {'$set': {'token': res['idToken']}})

    return jsonify({'token': res['idToken']}), 200


@AUTH_BP.route('/signout', methods=['POST'])
def signout():
    token = request.json['token']

    user = users.find_one({'token': token})
    if not user:
        return jsonify({'error': 'Invalid token'}), 400

    new_token = create_access_token(identity=user['token'])
    users.update_one({'token': token}, {'$set': {'token': new_token}})

    return jsonify({'done': 'success'}), 200


@AUTH_BP.route('/delete_account', methods=['POST'])
def delete_account():
    token = request.json['token']
    password = request.json['password']
    if not password:
        return jsonify({'error': 'Missing password'}), 400
    confirmPassword = request.json['confirmPassword']
    if not confirmPassword:
        return jsonify({'error': 'Missing confirmPassword'}), 400

    if password != confirmPassword:
        return jsonify({'error': 'Passwords do not match'}), 400

    user = users.find_one({'token': token})
    if not user:
        return jsonify({'error': 'Invalid token'}), 400

    email = user['email']
    # パスワードの認証
    firebase_api_key = settings.firebase_api_key
    res = firebase.sign_in_with_email_and_password(
        firebase_api_key, email, password)

    if 'error' in res:
        return jsonify({'error': res['error']['message']}), 400

    try:
        auth.delete_user(user['uid'])
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    users.delete_many({'uid': user['uid']})

    return jsonify({'done': 'success'}), 200
