import firebase_admin
from firebase_admin import credentials, auth
from flask import Flask, request, jsonify
from settings import Settings
from os.path import join, dirname
from flask_jwt_extended import JWTManager, create_access_token
from pymongo import MongoClient


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
        'password': password,
        'token': access_token
    }
    res = users.insert_one(user)

    if not res:
        return jsonify({'error': 'Failed to insert user'}), 400

    return jsonify({'token': access_token}), 200


if __name__ == '__main__':
    app.run()
