import firebase_admin
from firebase_admin import credentials
import firebase_admin.auth
from flask import Flask
from settings import Settings
from os.path import join, dirname
from flask_jwt_extended import JWTManager
from Auth.routes import AUTH_BP
from User.routes import USER_BP
from Pairing.routes import PAIRING_BP
from StreetPass.routes import STREETPASS_BP
from Notification.routes import NOTIFICATION_BP
from Child.routes import CHILD_BP
from LostChild.routes import LOSTCHILD_BP
import init_server

import logging
from handlers import DiscordHandler


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

# init server
init_server.db_init()

# Blueprint
app.register_blueprint(AUTH_BP)
app.register_blueprint(USER_BP)
app.register_blueprint(PAIRING_BP)
app.register_blueprint(STREETPASS_BP)
app.register_blueprint(NOTIFICATION_BP)
app.register_blueprint(CHILD_BP)
app.register_blueprint(LOSTCHILD_BP)

webhook_url = settings.log_webhook_url

# Discord Handler の作成
if (webhook_url):
    discord_handler = DiscordHandler(webhook_url)
    discord_handler.setLevel(logging.INFO)
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.addHandler(discord_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    werkzeug_logger.addHandler(console_handler)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8181)
