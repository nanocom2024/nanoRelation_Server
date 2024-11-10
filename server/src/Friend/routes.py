from flask import Blueprint, request, jsonify
from DB import DB

import manageFriend

FRIEND_BP = Blueprint('friend', __name__, url_prefix='/friend')

# MongoDBに接続
db = DB()

@FRIEND_BP.route('/add', methods=['POST'])
def add_friend():
    req_token = request.json['token']
    if not req_token: return jsonify({'error': 'Missing token'}), 400

    req_users = request.json['Users']
    if not req_users: return jsonify({'error': 'User not defined'}), 400

    for user in req_users:
        if not user['name']: return jsonify({'error': 'UserName not defined'}), 400
        if not user['id']: return jsonify({'error': 'UserID not defined'}), 400

        uid = db.users.find_one({'token': req_token})['uid']
        manageFriend.add_friend(uid, user['uid'])

    return jsonify({'message': 'Success'}), 200

@FRIEND_BP.route('/get', methods=['POST'])
def get_friend():
    req_token = request.json['token']
    if not req_token: return jsonify({'error': 'Missing token'}), 400

    uid = db.users.find_one({'token': req_token})['uid']
    friends = manageFriend.get_friends(uid)

    return jsonify({'friends': friends}), 200

# TODO: getだけどPOSTでいいのか？
@FRIEND_BP.route('/delete', methods=['POST'])
def delete_friend():
    req_token = request.json['token']
    if not req_token: return jsonify({'error': 'Missing token'}), 400

    req_users = request.json['Users']
    if not req_users: return jsonify({'error': 'User not defined'}), 400

    for user in req_users:
        if not user['name']: return jsonify({'error': 'UserName not defined'}), 400
        if not user['id']: return jsonify({'error': 'UserID not defined'}), 400

        uid = db.users.find_one({'token': req_token})['uid']
        manageFriend.remove_friend(uid, user['uid'])

    return jsonify({'message': 'Success'}), 200