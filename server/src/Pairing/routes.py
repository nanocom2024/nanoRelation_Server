
from flask import Blueprint, request, jsonify
from DB import DB
from crypto.generate import generate_ed25519_keypair
from flask_jwt_extended import create_access_token

PAIRING_BP = Blueprint('pairing', __name__, url_prefix='/pairing')

# MongoDBに接続
db = DB()
users = db.users
device_keys = db.device_keys
pre_pairings = db.pre_pairings
pairings = db.pairings


@PAIRING_BP.route('/generate_device_key', methods=['POST'])
def generate_device_key():
    uid = request.json['uid']
    if not uid:
        return jsonify({'error': 'Missing uid'}), 400

    if device_keys.find_one({'uid': uid}):
        return jsonify({'error': 'Device key already exists'}), 400

    private_key, public_key = generate_ed25519_keypair()

    device_keys.insert_one({
        'uid': uid,
        'private_key': private_key,
        'public_key': public_key
    })

    return jsonify({'private_key': private_key, 'public_key': public_key}), 200


@PAIRING_BP.route('/register_pairing', methods=['POST'])
def register_pairing():
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400
    public_key = request.json['public_key']
    if not public_key:
        return jsonify({'error': 'Missing public_key'}), 400

    user = users.find_one({'token': token})
    if not user:
        return jsonify({'error': 'Invalid token'}), 400

    device_key = device_keys.find_one({'public_key': public_key})
    if not device_key:
        return jsonify({'error': 'Invalid public_key'}), 400

    pre_pairings.insert_one({
        'uid': user['uid'],
        'public_key': public_key
    })

    return jsonify({'done': 'pre_pairing'}), 200


@PAIRING_BP.route('/check_pairing', methods=['POST'])
def check_pairing():
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400
    private_key = request.json['private_key']
    if not private_key:
        return jsonify({'error': 'Missing private_key'}), 400

    user = users.find_one({'token': token})
    if not user:
        return jsonify({'error': 'Invalid token'}), 400

    device_key = device_keys.find_one({'private_key': private_key})
    if not device_key:
        return jsonify({'error': 'Invalid private_key'}), 400

    pre_pairing = pre_pairings.find_one(
        {'uid': user['uid'], 'public_key': device_key['public_key']})

    if not pre_pairing:
        return jsonify({'error': 'Invalid pairing'}), 400

    pre_pairings.delete_many(
        {'uid': user['uid'], 'public_key': device_key['public_key']})

    pairings.delete_many({'uid': user['uid']})
    pairings.delete_many({'public_key': device_key['public_key']})
    pairings.delete_many({'private_key': private_key})

    pairings.insert_one({
        'uid': user['uid'],
        'public_key': device_key['public_key'],
        'private_key': private_key
    })

    return jsonify({'done': 'success'}), 200


@PAIRING_BP.route('/auth_check', methods=['POST'])
def auth_check():
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400

    user = users.find_one({'token': token})
    if not user:
        return jsonify({'error': 'Invalid token'}), 400

    new_token = create_access_token(identity=user['token'])
    users.update_one({'token': token}, {'$set': {'token': new_token}})

    return jsonify({'token': new_token}), 200
