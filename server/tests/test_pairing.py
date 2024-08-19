import requests
from pymongo import MongoClient

private_key = ''
public_key = ''
token = ''


def test_generate_device_key_success():
    global private_key
    global public_key
    url = 'http://127.0.0.1:5000/generate_device_key'
    res = requests.post(url, json={
        'uid': 'test_uid',
    })
    assert res.status_code == 200
    private_key = res.json()['private_key']
    public_key = res.json()['public_key']
    assert private_key
    assert public_key


def test_generate_device_key_missing_uid():
    url = 'http://127.0.0.1:5000/generate_device_key'
    res = requests.post(url, json={
        'uid': '',
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing uid'


def test_generate_device_key_already_exists():
    url = 'http://127.0.0.1:5000/generate_device_key'
    res = requests.post(url, json={
        'uid': 'test_uid',
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Device key already exists'


def get_token():
    url = 'http://127.0.0.1:5000/auth/signup'
    res = requests.post(url, json={
        'name': 'test',
        'email': 'test@test.org',
        'password': 'password'
    })
    token = res.json()['token']
    return token


def test_register_pairing_success():
    global token
    global public_key
    url = 'http://127.0.0.1:5000/register_pairing'
    token = get_token()
    res = requests.post(url, json={
        'token': token,
        'public_key': public_key
    })
    assert res.status_code == 200
    assert res.json()['done'] == 'pre_pairing'


def test_register_pairing_missing_token():
    global public_key
    url = 'http://127.0.0.1:5000/register_pairing'
    res = requests.post(url, json={
        'token': '',
        'public_key': public_key
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing token'


def test_register_pairing_missing_public_key():
    global token
    url = 'http://127.0.0.1:5000/register_pairing'
    res = requests.post(url, json={
        'token': token,
        'public_key': ''
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing public_key'


def test_register_pairing_invalid_token():
    global public_key
    url = 'http://127.0.0.1:5000/register_pairing'
    res = requests.post(url, json={
        'token': 'invalidToken',
        'public_key': public_key
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid token'


def test_register_pairing_invalid_public_key():
    global token
    url = 'http://127.0.0.1:5000/register_pairing'
    res = requests.post(url, json={
        'token': token,
        'public_key': 'invalidPublicKey'
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid public_key'


def test_check_pairing_missing_token():
    global private_key
    url = 'http://127.0.0.1:5000/check_pairing'
    res = requests.post(url, json={
        'token': '',
        'private_key': private_key
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing token'


def test_check_pairing_missing_private_key():
    global token
    url = 'http://127.0.0.1:5000/check_pairing'
    res = requests.post(url, json={
        'token': token,
        'private_key': ''
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing private_key'


def test_check_pairing_invalid_token():
    global private_key
    url = 'http://127.0.0.1:5000/check_pairing'
    res = requests.post(url, json={
        'token': 'invalidToken',
        'private_key': private_key
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid token'


def test_check_pairing_invalid_private_key():
    global token
    url = 'http://127.0.0.1:5000/check_pairing'
    res = requests.post(url, json={
        'token': token,
        'private_key': 'invalidPrivateKey'
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid private_key'


def test_check_pairing_success():
    global token
    global private_key
    url = 'http://127.0.0.1:5000/check_pairing'
    res = requests.post(url, json={
        'token': token,
        'private_key': private_key
    })
    assert res.status_code == 200
    assert res.json()['done'] == 'success'


def test_check_pairing_invalid_pairing():
    global token
    global private_key
    url = 'http://127.0.0.1:5000/check_pairing'
    res = requests.post(url, json={
        'token': token,
        'private_key': private_key
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid pairing'


def test_auth_check_success():
    global token
    url = 'http://127.0.0.1:5000/auth_check'
    res = requests.post(url, json={
        'token': token
    })
    assert res.status_code == 200
    token = res.json()['token']
    assert token


def test_auth_check_missing_token():
    url = 'http://127.0.0.1:5000/auth_check'
    res = requests.post(url, json={
        'token': ''
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Missing token'


def test_auth_check_invalid_token():
    url = 'http://127.0.0.1:5000/auth_check'
    res = requests.post(url, json={
        'token': 'invalidToken'
    })
    assert res.status_code == 400
    assert res.json()['error'] == 'Invalid token'


def test_done():
    global token
    client = MongoClient('localhost', 27017)
    db = client['db']

    device_keys = db['device_keys']
    device_keys.delete_many({'uid': 'test_uid'})
    assert not device_keys.find_one({'uid': 'test_uid'})

    users = db['users']
    user = users.find_one({'token': token})
    pre_pairings = db['pre_pairings']
    pre_pairings.delete_many({'uid': user['uid']})
    assert not pre_pairings.find_one({'uid': user['uid']})

    pairings = db['pairings']
    pairings.delete_many({'uid': user['uid']})
    assert not pairings.find_one({'uid': user['uid']})

    url = 'http://127.0.0.1:5000/auth/delete_account'
    requests.post(url, json={
        'password': 'password',
        'confirmPassword': 'password',
        'token': token
    })
    users.delete_many({'token': token})
    assert not users.find_one({'token': token})

    client.close()
