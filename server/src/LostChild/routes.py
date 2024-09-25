from datetime import datetime
from flask import Blueprint, request, jsonify
from DB import DB
from LostChild.LostChildrenModel import add_lost, delete_lost, is_lost_child
from Child.ChildrenModel import is_registered_child
from LostChild.LogLostChildrenModel import add_log_lost, get_log_lost

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


@LOSTCHILD_BP.route('/isLost', methods=['POST'])
def isLost():
    # childのuid
    uid = request.json['uid']
    if not uid:
        return jsonify({'error': 'Missing uid'}), 400

    # childの認証
    child = users.find_one({'uid': uid})
    if not child:
        return jsonify({'error': 'Invalid uid'}), 400

    pairing = pairings.find_one({'uid': child['uid']})

    if not pairing:
        return jsonify({'error': '子供のデバイスのペアリングを行なってください'}), 400

    if is_lost_child(pairing['major'], pairing['minor']):
        return jsonify({'is_lost': 'true'}), 200

    return jsonify({'is_lost': 'false'}), 200


@LOSTCHILD_BP.route('/add_message', methods=['POST'])
def add_message():
    # parentのtoken
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400
    # childのuid
    uid = request.json['uid']
    if not uid:
        return jsonify({'error': 'Missing uid'}), 400
    # msg
    msgID = request.json['msgID']
    if not msgID:
        return jsonify({'error': 'Missing msgID'}), 400
    text = request.json['text']
    if not text:
        return jsonify({'error': 'Missing text'}), 400
    tag = request.json['tag']
    if not tag:
        return jsonify({'error': 'Missing tag'}), 400
    timestamp = request.json['timestamp']
    if not timestamp:
        return jsonify({'error': 'Missing timestamp'}), 400
    # date_object = datetime.fromtimestamp(timestamp)

    # tokenの認証(parent)
    parent = users.find_one({'token': token})
    if not parent:
        return jsonify({'error': 'Invalid token'}), 401

    # childの認証
    child = users.find_one({'uid': uid})
    if not child:
        return jsonify({'error': 'Invalid uid'}), 400

    pairing = pairings.find_one({'uid': child['uid']})
    if not pairing:
        return jsonify({'error': '子供のデバイスのペアリングを行なってください'}), 400

    add_log_lost(child_uid=uid, msgID=msgID, tag=tag,
                 text=text, timestamp=timestamp)

    return jsonify({'done': 'Message added'}), 200


@LOSTCHILD_BP.route('/fetch_messages', methods=['POST'])
def fetch_messages():
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

    pairing = pairings.find_one({'uid': child['uid']})
    if not pairing:
        return jsonify({'error': '子供のデバイスのペアリングを行なってください'}), 400

    log = get_log_lost(child_uid=uid)
    if not log:
        return jsonify({'messages': []}), 200
    messages = log['messages']

    return jsonify({'messages': messages}), 200
