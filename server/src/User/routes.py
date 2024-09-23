from flask import Blueprint, request, jsonify
from DB import DB

USER_BP = Blueprint('user', __name__, url_prefix='/user')

# MongoDBに接続
db = DB()


@USER_BP.route('/fetch_users', methods=['POST'])
def fetch_users():
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400

    user = db.users.find_one({'token': token})
    if not user:
        return jsonify({'error': 'Invalid token'}), 400

    users = db.users.find()
    if not users:
        return jsonify({'users': []}), 200

    users_list = [{'uid': user['uid'], 'name': user['name'],
                   'name_id': user['name_id']} for user in users]
    return jsonify({'users': users_list}), 200
