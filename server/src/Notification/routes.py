from flask import Blueprint, request, jsonify
from DB import DB
from Notification.NotificationModel import enable, disable

NOTIFICATION_BP = Blueprint(
    'notification', __name__, url_prefix='/notification')

# MongoDBに接続
db = DB()
users = db.users


@NOTIFICATION_BP.route('/enable_notification', methods=['POST'])
def enable_notification():
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400
    enable_uid = request.json['enable_uid']
    if not enable_uid:
        return jsonify({'error': 'Missing enable_uid'}), 400

    req_user = users.find_one({'token': token})
    if not req_user:
        return jsonify({'error': 'Invalid token'}), 400
    target_user = users.find_one({'uid': enable_uid})
    if not target_user:
        return jsonify({'error': 'Invalid enable_uid'}), 400

    enable(req_user, target_user)
    return jsonify({'done': 'enable'}), 200


@NOTIFICATION_BP.route('/disable_notification', methods=['POST'])
def disable_notification():
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400
    disable_uid = request.json['disable_uid']
    if not disable_uid:
        return jsonify({'error': 'Missing disable_uid'}), 400

    req_user = users.find_one({'token': token})
    if not req_user:
        return jsonify({'error': 'Invalid token'}), 400
    target_user = users.find_one({'uid': disable_uid})
    if not target_user:
        return jsonify({'error': 'Invalid disable_uid'}), 400

    disable(req_user, target_user)
    return jsonify({'done': 'disable'}), 200
