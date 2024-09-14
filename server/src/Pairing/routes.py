
from flask import Blueprint, request, jsonify
from DB import DB
from crypto.generate import generate_ed25519_keypair
from Pairing import PairingModel
from flask_jwt_extended import create_access_token

PAIRING_BP = Blueprint('pairing', __name__, url_prefix='/pairing')

# MongoDBに接続
db = DB()
users = db.users
device_keys = db.device_keys
pairings = db.pairings


@PAIRING_BP.route('/generate_major_minor', methods=['POST'])
def generate_major_minor():
    uid = request.json['uid']
    if not uid:
        return jsonify({'error': 'Missing uid'}), 400

    if device_keys.find_one({'uid': uid}):
        return jsonify({'error': 'Device key already exists'}), 400

    private_key, public_key = generate_ed25519_keypair()

    major, minor = PairingModel.generate_major_minor(public_key)

    device_keys.insert_one({
        'uid': uid,
        'private_key': private_key,
        'public_key': public_key,
        'major': major,
        'minor': minor
    })

    return jsonify({
        'private_key': private_key,
        'public_key': public_key,
        'major': major,
        'minor': minor
    }), 200


@PAIRING_BP.route('/register_pairing', methods=['POST'])
def register_pairing():
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400
    major = request.json['major']
    if not major:
        return jsonify({'error': 'Missing major'}), 400
    minor = request.json['minor']
    if not minor:
        return jsonify({'error': 'Missing minor'}), 400

    user = users.find_one({'token': token})
    if not user:
        return jsonify({'error': 'Invalid token'}), 400

    device_key = device_keys.find_one({'major': major, 'minor': minor})
    if not device_key:
        return jsonify({'error': 'Invalid major,minor'}), 400

    pairings.delete_many({'uid': user['uid']})
    pairings.delete_many({'public_key': device_key['public_key']})
    pairings.delete_many({'private_key': device_key['private_key']})

    pairings.insert_one({
        'uid': user['uid'],
        'private_key': device_key['private_key'],
        'public_key': device_key['public_key'],
        'major': major,
        'minor': minor
    })

    return jsonify({'done': 'pairing'}), 200


@PAIRING_BP.route('/auth_check', methods=['POST'])
def auth_check():
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400

    user = users.find_one({'token': token})
    if not user:
        return jsonify({'error': 'Invalid token'}), 401

    new_token = create_access_token(identity=user['token'])
    users.update_one({'token': token}, {'$set': {'token': new_token}})

    return jsonify({'token': new_token}), 200
