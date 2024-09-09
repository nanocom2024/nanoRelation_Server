import requests
from pymongo import MongoClient


token1 = 'test_token1'
uid1 = 'test_uid1'

token2 = 'test_token2'
uid2 = 'test_uid2'

token3 = 'test_token3'
uid3 = 'test_uid3'


def test_insert_users():
    global token1, uid1
    global token2, uid2
    global token3, uid3
    client = MongoClient('localhost', 27017)
    db = client['db']
    users = db['users']
    users.insert_one({'uid': uid1, 'token': token1})
    users.insert_one({'uid': uid2, 'token': token2})
    users.insert_one({'uid': uid3, 'token': token3})
    client.close()


def test_disable_notification_missing_token(baseurl):
    global uid1
    url = baseurl+'/notification/disable_notification'
    res = requests.post(url, json={
        'token': '',
        'disable_uid': uid1
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing token'


def test_disable_notification_missing_disable_uid(baseurl):
    global token1
    url = baseurl+'/notification/disable_notification'
    res = requests.post(url, json={
        'token': token1,
        'disable_uid': ''
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing disable_uid'


def test_disable_notification_invalid_token(baseurl):
    global uid1
    url = baseurl+'/notification/disable_notification'
    res = requests.post(url, json={
        'token': 'invalidToken',
        'disable_uid': uid1
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid token'


def test_disable_notification_invalid_disable_uid(baseurl):
    global token1
    url = baseurl+'/notification/disable_notification'
    res = requests.post(url, json={
        'token': token1,
        'disable_uid': 'invalidUid'
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid disable_uid'


def test_disable_notification_success(baseurl):
    global token1
    global uid2, uid3
    url = baseurl+'/notification/disable_notification'
    res = requests.post(url, json={
        'token': token1,
        'disable_uid': uid2
    })
    assert res.status_code == 200
    assert res.json()['done'] == 'disable'

    res = requests.post(url, json={
        'token': token1,
        'disable_uid': uid3
    })
    assert res.status_code == 200
    assert res.json()['done'] == 'disable'

    client = MongoClient('localhost', 27017)
    db = client['db']
    notification_config = db['notification_config']
    data = notification_config.find_one({'owner': uid1})
    assert data['disables'] == [uid2, uid3]


def test_enable_notification_missing_token(baseurl):
    global uid1
    url = baseurl+'/notification/enable_notification'
    res = requests.post(url, json={
        'token': '',
        'enable_uid': uid1
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing token'


def test_enable_notification_missing_enable_uid(baseurl):
    global token1
    url = baseurl+'/notification/enable_notification'
    res = requests.post(url, json={
        'token': token1,
        'enable_uid': ''
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing enable_uid'


def test_enable_notification_invalid_token(baseurl):
    global uid1
    url = baseurl+'/notification/enable_notification'
    res = requests.post(url, json={
        'token': 'invalidToken',
        'enable_uid': uid1
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid token'


def test_enable_notification_invalid_enable_uid(baseurl):
    global token1
    url = baseurl+'/notification/enable_notification'
    res = requests.post(url, json={
        'token': token1,
        'enable_uid': 'invalidUid'
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid enable_uid'


def test_enable_notification_success(baseurl):
    global token1
    global uid2, uid3
    url = baseurl+'/notification/enable_notification'
    res = requests.post(url, json={
        'token': token1,
        'enable_uid': uid2
    })
    assert res.status_code == 200
    assert res.json()['done'] == 'enable'

    res = requests.post(url, json={
        'token': token1,
        'enable_uid': uid3
    })
    assert res.status_code == 200
    assert res.json()['done'] == 'enable'

    client = MongoClient('localhost', 27017)
    db = client['db']
    notification_config = db['notification_config']
    data = notification_config.find_one({'owner': uid1})
    assert data['disables'] == []


def test_done():
    global token1, uid1
    global token2, uid2
    global token3, uid3
    client = MongoClient('localhost', 27017)
    db = client['db']
    users = db['users']

    users.delete_many({'owner': uid1})
    users.delete_many({'owner': uid2})
    users.delete_many({'owner': uid3})
    assert not users.find_one({'owner': uid1})
    assert not users.find_one({'owner': uid2})
    assert not users.find_one({'owner': uid3})
    users.delete_many({'token': token1})
    users.delete_many({'token': token2})
    users.delete_many({'token': token3})
    assert not users.find_one({'token': token1})
    assert not users.find_one({'token': token2})
    assert not users.find_one({'token': token3})

    notification_config = db['notification_config']
    notification_config.delete_many({'owner': uid1})
    assert not notification_config.find_one({'owner': uid1})

    client.close()
