from pymongo import MongoClient

# MongoDBに接続
client = MongoClient("localhost", 27017)

db = client["db"]
users = db["users"]
device_keys = db["device_keys"]
pairings = db["pairings"]

# config
user_uid = "for_iBeacon_debug_user_uid"
name = "for_iBeacon_debug_name"
email = "for_iBeacon_debug_email@test.org"
token = "for_iBeacon_debug_token"

device_uid = "for_iBeacon_debug_device_uid"
private_key = "for_iBeacon_debug_private_key"
public_key = "for_iBeacon_debug_public_key"
major = "1"
minor = "1"


def insert_user():
    user = {
        'uid': user_uid,
        'name': name,
        'email': email,
        'token': token
    }
    res = users.insert_one(user)
    if not res:
        print("Failed to insert user")
        exit(1)


def insert_device_key():
    device_key = {
        'uid': device_uid,
        'private_key': private_key,
        'public_key': public_key,
        'major': major,
        'minor': minor
    }
    res = device_keys.insert_one(device_key)
    if not res:
        print("Failed to insert device key")
        exit(1)


def insert_pairing():
    pairing = {
        'uid': user_uid,
        'private_key': private_key,
        'public_key': public_key,
        'major': major,
        'minor': minor
    }
    res = pairings.insert_one(pairing)
    if not res:
        print("Failed to insert pairing")
        exit(1)


if __name__ == "__main__":
    insert_user()
    insert_device_key()
    insert_pairing()
