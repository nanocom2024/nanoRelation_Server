from flask import Blueprint, request, jsonify
from DB import DB
import datetime
from StreetPass.NotificationModel import check_notification_allowed

STREETPASS_BP = Blueprint('streetpass', __name__, url_prefix='/streetpass')

# MongoDBに接続
db = DB()
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
    private_key = request.json['private_key']
    if not private_key:
        return jsonify({'error': 'Missing private_key'}), 400

    received_user = pairings.find_one(
        {'major': received_major, 'minor': received_minor})
    if not received_user:
        return jsonify({'error': 'Invalid received_major_minor'}), 400
    sent_user = pairings.find_one({'private_key': private_key})
    if not sent_user:
        return jsonify({'error': 'Invalid private_key'}), 400

    if received_user['uid'] == sent_user['uid']:
        return jsonify({'pass': 'own'}), 200

    threshold = datetime.datetime.now() - datetime.timedelta(seconds=30)
    pre_passes.delete_many({'created_at': {'$lt': threshold}})
    threshold = datetime.datetime.now() - datetime.timedelta(seconds=60)
    now_passes.delete_many({'created_at': {'$lt': threshold}})

    uid1 = min(received_user['uid'], sent_user['uid'])
    uid2 = max(received_user['uid'], sent_user['uid'])

    if now_passes.find_one({'uid1': uid1, 'uid2': uid2}) and check_notification_allowed(sent_user, received_user):
        return jsonify({'pass': 'true'}), 200
    if pre_passes.find_one({'sent_uid': received_user['uid'], 'received_uid': sent_user['uid']}) and check_notification_allowed(sent_user, received_user):
        data = {
            'uid1': uid1,
            'uid2': uid2,
            'created_at': datetime.datetime.now()
        }
        now_passes.insert_one(data)
        log_passes.insert_one(data)
        return jsonify({'pass': 'true'}), 200
    pre_passes.insert_one(
        {'sent_uid': sent_user['uid'], 'received_uid': received_user['uid'], 'created_at': datetime.datetime.now()})
    return jsonify({'pass': 'false'}), 200
