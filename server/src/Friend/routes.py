from flask import Blueprint, request, jsonify
from DB import DB

FRIEND_BP = Blueprint('friend', __name__, url_prefix='/friend')

# MongoDBに接続
db = DB()

@FRIEND_BP.route('/add', methods=['POST'])
def add_friend():
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400
    
    uids = request.json['uids']
    if not uids:
        return jsonify({'error': 'Missing uids'}), 400

@FRIEND_BP.route('/get', methods=['POST'])
def add_friend():
    pass

@FRIEND_BP.route('/delete', methods=['POST'])
def add_friend():
    pass