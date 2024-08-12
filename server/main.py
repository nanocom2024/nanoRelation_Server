import firebase_admin
from firebase_admin import credentials, auth
from flask import Flask, request, jsonify
from settings import Settings
from os.path import join, dirname
from flask_jwt_extended import JWTManager, create_access_token


# Settings インスタンス
settings = Settings(join(dirname(__file__), '.env'))

path_to_firebase_json = settings.path_to_firebase_json
cred = credentials.Certificate(path_to_firebase_json)
firebase_admin.initialize_app(cred)
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = settings.jwt_secret_key      # JWTに署名する際の秘密鍵
app.config['JWT_ALGORITHM'] = 'HS256'                       # 暗号化署名のアルゴリズム

jwt = JWTManager(app)


@app.route('/signup', methods=['POST'])
def signup():
    email = request.json['email']
    if not email:
        return jsonify({'error': 'Missing email'}), 400
    password = request.json['password']
    if not password:
        return jsonify({'error': 'Missing password'}), 400

    try:
        user = auth.create_user(email=email, password=password)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    access_token = create_access_token(identity=user.uid)
    return jsonify({'token': access_token}), 200


if __name__ == '__main__':
    app.run()