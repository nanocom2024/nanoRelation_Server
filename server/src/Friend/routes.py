from flask import Blueprint, request, jsonify
from DB import DB

from Friend import manageFriend

FRIEND_BP = Blueprint('friend', __name__, url_prefix='/friend')

# MongoDBに接続
db = DB()

@FRIEND_BP.route('/add', methods=['POST'])
def add_friend():
    if not 'token' in request.json : return jsonify({'error': 'Missing token'}), 400
    req_token = request.json['token']

    if not 'users' in request.json: return jsonify({'error': 'User not defined'}), 400
    req_users = request.json['users']

    if not req_users: return jsonify({'error': 'User not defined'}), 400

    for user in req_users:
        if not 'name' in user: return jsonify({'error': 'UserName not defined'}), 400
        if not 'id' in user: return jsonify({'error': 'UserID not defined'}), 400

        uid = db.users.find_one({'token': req_token})['uid']
        manageFriend.add_friend(uid, user['uid'])

    return jsonify({'message': 'Success'}), 200

@FRIEND_BP.route('/get', methods=['POST'])
def get_friend():
    if not 'token' in request.json: return jsonify({'error': 'Missing token'}), 400
    req_token = request.json['token']

    uid = db.users.find_one({'token': req_token})['uid']
    friends = manageFriend.get_friends(uid)

    return jsonify({'friends': friends}), 200

# TODO: getだけどPOSTでいいのか？
@FRIEND_BP.route('/delete', methods=['POST'])
def delete_friend():
    if not 'token' in request.json: return jsonify({'error': 'Missing token'}), 400
    req_token = request.json['token']

    if not 'users' in request.json: return jsonify({'error': 'User not defined'}), 400
    req_users = request.json['users']

    if not req_users: return jsonify({'error': 'User not defined'}), 400

    for user in req_users:
        if 'name' not in user: return jsonify({'error': 'UserName not defined'}), 400
        if 'id' not in user: return jsonify({'error': 'UserID not defined'}), 400

        uid = db.users.find_one({'token': req_token})['uid']
        manageFriend.remove_friend(uid, user['uid'])

    return jsonify({'message': 'Success'}), 200