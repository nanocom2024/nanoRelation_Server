import firebase_admin
from firebase_admin import credentials
import firebase_admin.auth
from flask import Flask
from settings import Settings
from os.path import join, dirname
from flask_jwt_extended import JWTManager
from DB import DB
from Auth.routes import AUTH_BP
from Pairing.routes import PAIRING_BP
from StreetPass.routes import STREETPASS_BP


# Settings インスタンス
settings = Settings(join(dirname(__file__), '../.env'))

# app
path_to_firebase_json = './../' + settings.path_to_firebase_json
cred = credentials.Certificate(path_to_firebase_json)
firebase_admin.initialize_app(cred)
app = Flask(__name__)

# config
app.config['JWT_SECRET_KEY'] = settings.jwt_secret_key      # JWTに署名する際の秘密鍵
app.config['JWT_ALGORITHM'] = 'HS256'                       # 暗号化署名のアルゴリズム

# jwt manager
jwt = JWTManager(app)


# Blueprint
app.register_blueprint(AUTH_BP)
app.register_blueprint(PAIRING_BP)
app.register_blueprint(STREETPASS_BP)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8181)
