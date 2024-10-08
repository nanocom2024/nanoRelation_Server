import os
from dotenv import load_dotenv


class Settings:
    def __init__(self, envpath):
        # .env ファイルを明示的に指定して環境変数として読み込む
        self.__dotenv_path = envpath
        load_dotenv(self.__dotenv_path)
        # 環境変数から設定値を取得
        self.__path_to_firebase_json = os.environ.get("PATH_TO_FIREBASE_JSON")
        self.__jwt_secret_key = os.environ.get("JWT_SECRET_KEY")
        self.__firebase_api_key = os.environ.get("FIREBASE_API_KEY")
        self.__log_webhook_url = os.environ.get("LOG_WEBHOOK_URL")

    # firebase の json
    @property
    def path_to_firebase_json(self):
        return self.__path_to_firebase_json

    # jwt の秘密鍵
    @property
    def jwt_secret_key(self):
        return self.__jwt_secret_key

    # firebase の api key
    @property
    def firebase_api_key(self):
        return self.__firebase_api_key
    
    # webhook url
    @property
    def log_webhook_url(self):
        return self.__log_webhook_url
