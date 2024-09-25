from flask import Blueprint, request, jsonify
from DB import DB
from User.LogModel import get_logs

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


@USER_BP.route('/fetch_user_log', methods=['POST'])
def fetch_user_log():
    # リクエストしているユーザーのtoken
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400
    # 相手のuid
    uid = request.json['uid']
    if not uid:
        return jsonify({'error': 'Missing uid'}), 400

    # tokenの認証(parent)
    request_user = db.users.find_one({'token': token})
    if not request_user:
        return jsonify({'error': 'Invalid token'}), 401

    # childの認証
    target_user = db.users.find_one({'uid': uid})
    if not target_user:
        return jsonify({'error': 'Invalid uid'}), 400

    logs = get_logs(
        request_uid=request_user['uid'], target_uid=target_user['uid'])
    if not logs:
        return jsonify({'logs': []}), 200

    return jsonify({'logs': logs}), 200
