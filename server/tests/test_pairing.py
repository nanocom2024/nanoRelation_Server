import random
import string
import requests
from pymongo import MongoClient

private_key = ''
public_key = ''
major = ''
minor = ''
token = ''
email = ''.join(random.choices(string.ascii_lowercase +
                string.digits, k=20))+'@test.org'


def test_generate_major_minor_success(baseurl):
    global private_key
    global public_key
    global major
    global minor
    url = baseurl+'/pairing/generate_major_minor'
    res = requests.post(url, json={
        'uid': 'test_uid',
    })
    assert res.status_code == 200
    private_key = res.json()['private_key']
    assert private_key
    public_key = res.json()['public_key']
    assert public_key
    major = res.json()['major']
    assert major
    minor = res.json()['minor']
    assert minor


def test_generate_major_minor_missing_uid(baseurl):
    url = baseurl+'/pairing/generate_major_minor'
    res = requests.post(url, json={
        'uid': '',
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing uid'


def test_generate_major_minor_already_exists(baseurl):
    url = baseurl+'/pairing/generate_major_minor'
    res = requests.post(url, json={
        'uid': 'test_uid',
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Device key already exists'


def get_token(baseurl):
    global email
    url = baseurl+'/auth/signup'
    res = requests.post(url, json={
        'name': 'test',
        'email': email,
        'password': 'password'
    })
    token = res.json()['token']
    return token


def test_register_pairing_success(baseurl):
    global token
    global major, minor
    url = baseurl+'/pairing/register_pairing'
    token = get_token(baseurl)
    res = requests.post(url, json={
        'token': token,
        'major': major,
        'minor': minor
    })
    assert res.status_code == 200
    assert res.json()['done'] == 'pairing'

    client = MongoClient('localhost', 27017)
    db = client['db']
    pairings = db['pairings']
    users = db['users']

    user = users.find_one({'token': token})
    pairing = pairings.find_one(
        {'uid': user['uid'], 'major': major, 'minor': minor})
    assert pairing


def test_register_pairing_missing_token(baseurl):
    global public_key
    global major, minor
    url = baseurl+'/pairing/register_pairing'
    res = requests.post(url, json={
        'token': '',
        'major': major,
        'minor': minor
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing token'


def test_register_pairing_missing_major(baseurl):
    global token
    global minor
    url = baseurl+'/pairing/register_pairing'
    res = requests.post(url, json={
        'token': token,
        'major': '',
        'minor': minor
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing major'


def test_register_pairing_missing_minor(baseurl):
    global token
    global major
    url = baseurl+'/pairing/register_pairing'
    res = requests.post(url, json={
        'token': token,
        'major': major,
        'minor': ''
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing minor'


def test_register_pairing_invalid_token(baseurl):
    global public_key
    global major, minor
    url = baseurl+'/pairing/register_pairing'
    res = requests.post(url, json={
        'token': 'invalidToken',
        'major': major,
        'minor': minor
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid token'


def test_register_pairing_invalid_major_minor(baseurl):
    global token
    global major, minor
    url = baseurl+'/pairing/register_pairing'
    res = requests.post(url, json={
        'token': token,
        'major': 'invalidMajor',
        'minor': minor
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid major,minor'

    res = requests.post(url, json={
        'token': token,
        'major': major,
        'minor': 'invalidMinor'
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid major,minor'


def test_auth_check_success(baseurl):
    global token
    url = baseurl+'/pairing/auth_check'
    res = requests.post(url, json={
        'token': token
    })
    assert res.status_code == 200
    token = res.json()['token']
    assert token


def test_auth_check_missing_token(baseurl):
    url = baseurl+'/pairing/auth_check'
    res = requests.post(url, json={
        'token': ''
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing token'


def test_auth_check_invalid_token(baseurl):
    url = baseurl+'/pairing/auth_check'
    res = requests.post(url, json={
        'token': 'invalidToken'
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid token'


def test_done(baseurl):
    global token
    global email
    client = MongoClient('localhost', 27017)
    db = client['db']

    device_keys = db['device_keys']
    device_keys.delete_many({'uid': 'test_uid'})
    assert not device_keys.find_one({'uid': 'test_uid'})

    users = db['users']
    user = users.find_one({'token': token})
    pairings = db['pairings']
    pairings.delete_many({'uid': user['uid']})
    assert not pairings.find_one({'uid': user['uid']})

    url = baseurl+'/auth/delete_account'
    requests.post(url, json={
        'password': 'password',
        'confirmPassword': 'password',
        'token': token
    })
    users.delete_many({'token': token})
    assert not users.find_one({'token': token})
    assert not users.find_one({'email': email})

    client.close()
