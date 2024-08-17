import firebase_admin
from firebase_admin import credentials, auth
import firebase_admin.auth
from flask import Flask, request, jsonify
from settings import Settings
from os.path import join, dirname
from flask_jwt_extended import JWTManager, create_access_token
from pymongo import MongoClient
from Auth import Auth
from crypto.generate import generate_ed25519_keypair


# Settings インスタンス
settings = Settings(join(dirname(__file__), '.env'))

# app
path_to_firebase_json = settings.path_to_firebase_json
cred = credentials.Certificate(path_to_firebase_json)
firebase_admin.initialize_app(cred)
app = Flask(__name__)

# config
app.config['JWT_SECRET_KEY'] = settings.jwt_secret_key      # JWTに署名する際の秘密鍵
app.config['JWT_ALGORITHM'] = 'HS256'                       # 暗号化署名のアルゴリズム

# jwt manager
jwt = JWTManager(app)

# MongoDBに接続
client = MongoClient("localhost", 27017)
db = client["db"]
users = db["users"]
device_keys = db["device_keys"]
pre_pairings = db["pre_pairings"]
pairings = db["pairings"]


@app.route('/signup', methods=['POST'])
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


@app.route('/signin', methods=['POST'])
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
    res = Auth.sign_in_with_email_and_password(
        firebase_api_key, email, password)

    if 'error' in res:
        return jsonify({'error': res['error']['message']}), 400

    users.update_one({'email': email}, {'$set': {'token': res['idToken']}})

    return jsonify({'token': res['idToken']}), 200


@app.route('/signout', methods=['POST'])
def signout():
    token = request.json['token']

    user = users.find_one({'token': token})
    if not user:
        return jsonify({'error': 'Invalid token'}), 400

    new_token = create_access_token(identity=user['token'])
    users.update_one({'token': token}, {'$set': {'token': new_token}})

    return jsonify({'done': 'success'}), 200


@app.route('/delete_account', methods=['POST'])
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

    try:
        auth.delete_user(user['uid'])
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    users.delete_many({'uid': user['uid']})

    return jsonify({'done': 'success'}), 200


@app.route('/generate_device_key', methods=['POST'])
def generate_device_key():
    uid = request.json['uid']
    if not uid:
        return jsonify({'error': 'Missing uid'}), 400

    if device_keys.find_one({'uid': uid}):
        return jsonify({'error': 'Device key already exists'}), 400

    private_key, public_key = generate_ed25519_keypair()

    device_keys.insert_one({
        'uid': uid,
        'private_key': private_key,
        'public_key': public_key
    })

    return jsonify({'private_key': private_key, 'public_key': public_key}), 200


@app.route('/register_pairing', methods=['POST'])
def register_pairing():
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400
    public_key = request.json['public_key']
    if not public_key:
        return jsonify({'error': 'Missing public_key'}), 400

    user = users.find_one({'token': token})
    if not user:
        return jsonify({'error': 'Invalid token'}), 400

    device_key = device_keys.find_one({'public_key': public_key})
    if not device_key:
        return jsonify({'error': 'Invalid public_key'}), 400

    pre_pairings.insert_one({
        'uid': user['uid'],
        'public_key': public_key
    })

    return jsonify({'done': 'pre_pairing'}), 200


@app.route('/check_pairing', methods=['POST'])
def check_pairing():
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400
    private_key = request.json['private_key']
    if not private_key:
        return jsonify({'error': 'Missing private_key'}), 400

    user = users.find_one({'token': token})
    if not user:
        return jsonify({'error': 'Invalid token'}), 400

    device_key = device_keys.find_one({'private_key': private_key})
    if not device_key:
        return jsonify({'error': 'Invalid private_key'}), 400

    pre_pairing = pre_pairings.find_one(
        {'uid': user['uid'], 'public_key': device_key['public_key']})

    if not pre_pairing:
        return jsonify({'error': 'Invalid pairing'}), 400

    pre_pairings.delete_many(
        {'uid': user['uid'], 'public_key': device_key['public_key']})

    pairings.delete_many({'uid': user['uid']})
    pairings.delete_many({'public_key': device_key['public_key']})
    pairings.delete_many({'private_key': private_key})

    pairings.insert_one({
        'uid': user['uid'],
        'public_key': device_key['public_key'],
        'private_key': private_key
    })

    return jsonify({'done': 'success'}), 200


@app.route('/auth_check', methods=['POST'])
def auth_check():
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400

    user = users.find_one({'token': token})
    if not user:
        return jsonify({'error': 'Invalid token'}), 400

    new_token = create_access_token(identity=user['token'])
    users.update_one({'token': token}, {'$set': {'token': new_token}})

    return jsonify({'token': new_token}), 200


if __name__ == '__main__':
    app.run()
