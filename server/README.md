# server

## 準備

FirebaseのAuthenticationを用いています

### 環境設定

.env

```env
PATH_TO_FIREBASE_JSON = "example"
JWT_SECRET_KEY = "example"
```

・Firebase Authenticationに従ってsdkのjsonを配置して，パスを設定してください

・serverの秘密鍵の設定もしてください

### ライブラリのインストール

```zsh
pip install -r requirements.txt
```

### 参考

[サーバーに Firebase Admin SDK を追加する](https://firebase.google.com/docs/admin/setup?hl=ja)

[Admin Auth API の概要](https://firebase.google.com/docs/auth/admin?hl=ja)

[Python の Flask Web API に JWT認証（Flask-JWT-Extended）を組み込んだ](https://qiita.com/kerobot/items/c5607658171c2aec4f46)

[PythonからFirebase認証を利用する(メール/パスワード認証編)](https://qiita.com/masatomix/items/239eef6b643ece537344)

[Firebase 認証 REST API](https://firebase.google.com/docs/reference/rest/auth?hl=ja)
