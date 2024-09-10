import pytest
import random
import string
import requests
from pymongo import MongoClient
import datetime

private_key1 = ''
public_key1 = ''
major1 = ''
minor1 = ''
token1 = ''
email1 = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=20))+'@test.org'
device_uid1 = 'test_uid1'

private_key2 = ''
public_key2 = ''
major2 = ''
minor2 = ''
token2 = ''
email2 = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=20))+'@test.org'
device_uid2 = 'test_uid2'


def test_signup_success(baseurl):
    global token1
    global email1
    url = baseurl+'/auth/signup'
    res = requests.post(url, json={
        'name': 'test',
        'email': email1,
        'password': 'password'
    })
    assert res.status_code == 200
    token1 = res.json()['token']
    assert token1

    global token2
    global email2
    res = requests.post(url, json={
        'name': 'test',
        'email': email2,
        'password': 'password'
    })
    assert res.status_code == 200
    token2 = res.json()['token']
    assert token2


def test_device_major_minor(baseurl):
    global device_uid1
    global private_key1
    global major1, minor1
    url = baseurl+'/pairing/generate_major_minor'
    res = requests.post(url, json={
        'uid': device_uid1,
    })
    assert res.status_code == 200
    private_key1 = res.json()['private_key']
    assert private_key1
    major1 = res.json()['major']
    assert major1
    minor1 = res.json()['minor']
    assert minor1

    global device_uid2
    global private_key2
    global major2, minor2
    url = baseurl+'/pairing/generate_major_minor'
    res = requests.post(url, json={
        'uid': device_uid2,
    })
    assert res.status_code == 200
    private_key2 = res.json()['private_key']
    assert private_key2
    major2 = res.json()['major']
    assert major2
    minor2 = res.json()['minor']
    assert minor2


def test_pairing_success(baseurl):
    global token1
    global private_key1
    url = baseurl+'/pairing/register_pairing'
    res = requests.post(url, json={
        'token': token1,
        'major': major1,
        'minor': minor1
    })
    assert res.status_code == 200
    assert res.json()['done'] == 'pairing'

    global token2
    global private_key2
    res = requests.post(url, json={
        'token': token2,
        'major': major2,
        'minor': minor2
    })
    assert res.status_code == 200
    assert res.json()['done'] == 'pairing'

    url = baseurl+'/pairing/auth_check'
    res = requests.post(url, json={
        'token': token1,
    })
    assert res.status_code == 200
    token1 = res.json()['token']
    assert token1

    res = requests.post(url, json={
        'token': token2,
    })
    assert res.status_code == 200
    token2 = res.json()['token']
    assert token2


def test_received_beacon_missing_received_major(baseurl):
    global private_key1
    url = baseurl+'/streetpass/received_beacon'
    res = requests.post(url, json={
        'received_major': '',
        'received_minor': minor1,
        'private_key': private_key1
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing received_major'


def test_received_beacon_missing_received_minor(baseurl):
    global private_key1
    url = baseurl+'/streetpass/received_beacon'
    res = requests.post(url, json={
        'received_major': major1,
        'received_minor': '',
        'private_key': private_key1
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing received_minor'


def test_received_beacon_missing_private_key(baseurl):
    url = baseurl+'/streetpass/received_beacon'
    res = requests.post(url, json={
        'received_major': major1,
        'received_minor': minor1,
        'private_key': ''
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing private_key'


def test_received_beacon_invalid_received_major_minor(baseurl):
    global private_key1
    url = baseurl+'/streetpass/received_beacon'
    res = requests.post(url, json={
        'received_major': major1,
        'received_minor': 'invalidMinor',
        'private_key': private_key1
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid received_major_minor'

    res = requests.post(url, json={
        'received_major': 'invalidMajor',
        'received_minor': minor1,
        'private_key': private_key1
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid received_major_minor'


def test_received_beacon_invalid_private_key(baseurl):
    url = baseurl+'/streetpass/received_beacon'
    res = requests.post(url, json={
        'received_major': major1,
        'received_minor': minor1,
        'private_key': 'invalidPrivateKey'
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid private_key'


def test_received_beacon_enable_success(baseurl):
    global private_key1
    url = baseurl+'/streetpass/received_beacon'
    res = requests.post(url, json={
        'received_major': major2,
        'received_minor': minor2,
        'private_key': private_key1
    })
    assert res.status_code == 200
    assert res.json()['pass'] == 'false'

    global private_key2
    res = requests.post(url, json={
        'received_major': major1,
        'received_minor': minor1,
        'private_key': private_key2
    })
    assert res.status_code == 200
    assert res.json()['pass'] == 'true'


def test_received_beacon_disable_success(baseurl):
    global token1, private_key1
    global token2, private_key2
    client = MongoClient('localhost', 27017)
    db = client['db']
    users = db['users']
    user2 = users.find_one({'token': token2})
    assert user2

    url = baseurl+'/notification/disable_notification'
    res = requests.post(url, json={
        'token': token1,
        'disable_uid': user2['uid']
    })
    assert res.status_code == 200
    assert res.json()['done'] == 'disable'

    url = baseurl+'/streetpass/received_beacon'
    res = requests.post(url, json={
        'received_major': major2,
        'received_minor': minor2,
        'private_key': private_key1
    })
    assert res.status_code == 200
    assert res.json()['pass'] == 'false'


def test_done():
    global token1, device_uid1, email1
    global token2, device_uid2, email2
    client = MongoClient('localhost', 27017)
    db = client['db']

    device_keys = db['device_keys']
    device_keys.delete_many({'uid': device_uid1})
    assert not device_keys.find_one({'uid': device_uid1})
    device_keys.delete_many({'uid': device_uid2})
    assert not device_keys.find_one({'uid': device_uid2})

    users = db['users']
    user1 = users.find_one({'token': token1})
    user2 = users.find_one({'token': token2})

    pairings = db['pairings']
    pairings.delete_many({'uid': user1['uid']})
    assert not pairings.find_one({'uid': user1['uid']})
    pairings.delete_many({'uid': user2['uid']})
    assert not pairings.find_one({'uid': user2['uid']})

    pre_passes = db['pre_passes']
    threshold = datetime.datetime.now() - datetime.timedelta(seconds=30)
    assert pre_passes.find_one({'created_at': {'$lt': threshold}}) is None
    assert pre_passes.find_one(
        {'sent_uid': user1['uid'], 'received_uid': user2['uid']})
    pre_passes.delete_many(
        {'sent_uid': user1['uid'], 'received_uid': user2['uid']})

    now_passes = db['now_passes']
    threshold = datetime.datetime.now() - datetime.timedelta(seconds=60)
    assert now_passes.find_one({'created_at': {'$lt': threshold}}) is None
    now_passes.delete_many({'uid1': user1['uid'], 'uid2': user2['uid']})
    assert not now_passes.find_one(
        {'uid1': user1['uid'], 'uid2': user2['uid']})
    now_passes.delete_many({'uid1': user2['uid'], 'uid2': user1['uid']})
    assert not now_passes.find_one(
        {'uid1': user2['uid'], 'uid2': user1['uid']})

    log_passes = db['log_passes']
    data = {
        'uid1': min(user1['uid'], user2['uid']),
        'uid2': max(user1['uid'], user2['uid']),
    }
    assert log_passes.find_one(data) is not None
    log_passes.delete_many(data)

    client.close()


def test_cleanup_users(baseurl):
    global token1, email1
    global token2, email2
    client = MongoClient('localhost', 27017)
    db = client['db']
    users = db['users']

    url = baseurl+'/auth/delete_account'
    requests.post(url, json={
        'password': 'password',
        'confirmPassword': 'password',
        'token': token1
    })
    users.delete_many({'token': token1})
    assert not users.find_one({'token': token1})
    assert not users.find_one({'email': email1})
    requests.post(url, json={
        'password': 'password',
        'confirmPassword': 'password',
        'token': token2
    })
    users.delete_many({'token': token2})
    assert not users.find_one({'token': token2})
    assert not users.find_one({'email': email2})

    client.close()
