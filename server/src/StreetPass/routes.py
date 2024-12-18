from flask import Blueprint, request, jsonify
from DB import DB
import datetime
from StreetPass.NotificationModel import check_notification_allowed
from LostChild.LostChildrenModel import is_lost_child
from Child.ChildrenModel import is_registered_child
from User.LogOwnModel import add_log_own
from User.LogLostPassesModel import add_log_lost_passes
from User.LogNearOwnChildrenModel import add_log_near_own_children

STREETPASS_BP = Blueprint('streetpass', __name__, url_prefix='/streetpass')

# MongoDBに接続
db = DB()
users = db.users
pairings = db.pairings
pre_passes = db.pre_passes
now_passes = db.now_passes
log_passes = db.log_passes


@STREETPASS_BP.route('/received_beacon', methods=['POST'])
def received_beacon():
    received_major = request.json['received_major']
    if not received_major:
        return jsonify({'error': 'Missing received_major'}), 400
    received_minor = request.json['received_minor']
    if not received_minor:
        return jsonify({'error': 'Missing received_minor'}), 400
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400
    # optional
    try:
        latitude = request.json['latitude']
        longitude = request.json['longitude']
    except Exception as e:
        latitude = 0
        longitude = 0

    received_user = pairings.find_one(
        {'major': received_major, 'minor': received_minor})
    if not received_user:
        return jsonify({'error': 'Invalid received_major_minor'}), 400
    sent_user = users.find_one({'token': token})
    if not sent_user:
        return jsonify({'error': 'Invalid token'}), 400

    if received_user['uid'] == sent_user['uid']:
        add_log_own(owner_uid=sent_user['uid'])
        return jsonify({'pass': 'own'}), 200

    # if is_lost_child(major=received_major, minor=received_minor):
    #     add_log_lost_passes(
    #         owner_uid=sent_user['uid'], child_uid=received_user['uid'], latitude=latitude, longitude=longitude)
    #     return jsonify({'pass': 'lost'}), 200

    if is_registered_child(parent_uid=sent_user['uid'], child_uid=received_user['uid']):
        add_log_near_own_children(
            parent_uid=sent_user['uid'], child_uid=received_user['uid'])
        return jsonify({'pass': 'child'}), 200

    threshold = datetime.datetime.now() - datetime.timedelta(seconds=30)
    pre_passes.delete_many({'created_at': {'$lt': threshold}})
    threshold = datetime.datetime.now().timestamp() - 60
    now_passes.delete_many({'timestamp': {'$lt': threshold}})

    uid1 = min(received_user['uid'], sent_user['uid'])
    uid2 = max(received_user['uid'], sent_user['uid'])

    if now_passes.find_one({'uid1': uid1, 'uid2': uid2}) and check_notification_allowed(sent_user, received_user):
        return jsonify({'pass': 'true'}), 200
    if pre_passes.find_one({'sent_uid': received_user['uid'], 'received_uid': sent_user['uid']}) and check_notification_allowed(sent_user, received_user):
        data = {
            'uid1': uid1,
            'uid2': uid2,
            'timestamp': datetime.datetime.now().timestamp()
        }
        now_passes.insert_one(data)
        log_passes.insert_one(data)
        return jsonify({'pass': 'true'}), 200
    pre_passes.insert_one(
        {'sent_uid': sent_user['uid'], 'received_uid': received_user['uid'], 'created_at': datetime.datetime.now()})
    return jsonify({'pass': 'false'}), 200


@STREETPASS_BP.route('/received_lost_beacon', methods=['POST'])
def received_lost_beacon():
    major = request.json['major']
    if not major:
        return jsonify({'error': 'Missing major'}), 400
    minor = request.json['minor']
    if not minor:
        return jsonify({'error': 'Missing minor'}), 400
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400
    # optional
    latitude = request.json['latitude'] if 'latitude' in request.json else 0
    longitude = request.json['longitude'] if 'longitude' in request.json else 0

    parent_user = db.observe_pairings.find_one(
        {'major': major, 'minor': minor})
    if not parent_user:
        return jsonify({'error': 'Invalid major_minor'}), 400
    provide_user = users.find_one({'token': token})
    if not provide_user:
        return jsonify({'error': 'Invalid token'}), 400

    add_log_lost_passes(
        provider_uid=provide_user['uid'], parent_uid=parent_user['uid'], latitude=latitude, longitude=longitude)
    return jsonify({'pass': 'ok'}), 200
