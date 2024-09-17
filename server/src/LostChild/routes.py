from flask import Blueprint, request, jsonify
from DB import DB
from LostChild.LostChildrenModel import add_lost, delete_lost
from LostChild.ChildrenModel import is_registered_child

LOSTCHILD_BP = Blueprint('lost_child', __name__, url_prefix='/lost_child')

db = DB()
users = db.users
pairings = db.pairings


@LOSTCHILD_BP.route('/register_lost', methods=['POST'])
def register_lost():
    # parentのtoken
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400
    # childのuid
    uid = request.json['uid']
    if not uid:
        return jsonify({'error': 'Missing uid'}), 400

    # tokenの認証(parent)
    parent = users.find_one({'token': token})
    if not parent:
        print('Invalid token')
        return jsonify({'error': 'Invalid token'}), 401

    # childの認証
    child = users.find_one({'uid': uid})
    if not child:
        print('Invalid uid')
        return jsonify({'error': 'Invalid uid'}), 400

    if not is_registered_child(parent_uid=parent['uid'], child_uid=child['uid']):
        print('Child not registered')
        return jsonify({'error': 'Child not registered'}), 400

    pairing = pairings.find_one({'uid': child['uid']})
    add_lost(pairing['major'], pairing['minor'])

    return jsonify({'done': 'Lost child registered'}), 200


@LOSTCHILD_BP.route('/delete_lost_info', methods=['POST'])
def delete_lost_info():
    # parentのtoken
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400
    # childのuid
    uid = request.json['uid']
    if not uid:
        return jsonify({'error': 'Missing uid'}), 400

    # tokenの認証(parent)
    parent = users.find_one({'token': token})
    if not parent:
        return jsonify({'error': 'Invalid token'}), 401

    # childの認証
    child = users.find_one({'uid': uid})
    if not child:
        return jsonify({'error': 'Invalid uid'}), 400

    if not is_registered_child(parent_uid=parent['uid'], child_uid=child['uid']):
        return jsonify({'error': 'Child not registered'}), 400

    pairing = pairings.find_one({'uid': child['uid']})
    delete_lost(pairing['major'], pairing['minor'])

    return jsonify({'done': 'Lost child deleted'}), 200
