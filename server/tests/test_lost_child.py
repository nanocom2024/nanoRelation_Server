import random
import string
from pymongo import MongoClient
import requests

client = MongoClient('localhost', 27017)
db = client['db']
users = db['users']
children = db['children']
lost_children = db['lost_children']
device_keys = db['device_keys']

# parent
parent_email = ''.join(random.choices(
    string.ascii_lowercase + string.digits, k=20))+'@test.org'
parent_token = ''

# child
child_uid = ''
child_email = ''.join(random.choices(
    string.ascii_lowercase + string.digits, k=20))+'@test.org'
child_token = ''
child_major = ''
child_minor = ''


def test_signup_success(baseurl):
    global parent_token, parent_email
    url = baseurl+'/auth/signup'
    res = requests.post(url, json={
        'name': 'test',
        'email': parent_email,
        'password': 'password'
    })
    assert res.status_code == 200
    parent_token = res.json()['token']
    assert parent_token

    global child_token, child_email
    res = requests.post(url, json={
        'name': 'test',
        'email': child_email,
        'password': 'password'
    })
    assert res.status_code == 200
    child_token = res.json()['token']
    assert child_token


def test_register_child_success(baseurl):
    global parent_token, child_uid
    url = baseurl+'/child/register_child'
    res = requests.post(url, json={
        'token': parent_token,
        'email': child_email,
        'password': 'password'
    })
    assert res.status_code == 200
    assert res.json()['done'] == 'register'


def test_generate_major_minor_success(baseurl):
    global child_major, child_minor
    url = baseurl+'/pairing/generate_major_minor'
    res = requests.post(url, json={
        'uid': 'test_child_device_uid',
    })
    assert res.status_code == 200
    assert res.json()['private_key']
    assert res.json()['public_key']
    child_major = res.json()['major']
    assert child_major
    child_minor = res.json()['minor']
    assert child_minor


def test_register_pairing_success(baseurl):
    global child_token
    global child_major, child_minor
    url = baseurl+'/pairing/register_pairing'
    child = users.find_one({'email': child_email})
    res = requests.post(url, json={
        'token': child['token'],
        'major': child_major,
        'minor': child_minor
    })
    assert res.status_code == 200
    assert res.json()['done'] == 'pairing'


def test_register_lost_success(baseurl):
    global parent_token
    global child_email, child_major, child_minor
    child = users.find_one({'email': child_email})
    url = baseurl+'/lost_child/register_lost'
    res = requests.post(url, json={
        'token': parent_token,
        'uid': child['uid']
    })
    assert res.status_code == 200
    assert res.json()['done'] == 'Lost child registered'

    lost = lost_children.find_one({'major': child_major, 'minor': child_minor})
    assert lost


def test_delete_lost_info_success(baseurl):
    global parent_token
    global child_email, child_major, child_minor
    child = users.find_one({'email': child_email})
    url = baseurl+'/lost_child/delete_lost_info'
    res = requests.post(url, json={
        'token': parent_token,
        'uid': child['uid']
    })
    assert res.status_code == 200
    assert res.json()['done'] == 'Lost child deleted'

    lost = lost_children.find_one({'major': child_major, 'minor': child_minor})
    assert not lost


def test_done():
    lost_children.delete_many({'major': child_major, 'minor': child_minor})
    device_keys.delete_many({'major': child_major, 'minor': child_minor})
    parent = users.find_one({'email': parent_email})
    children.delete_many({'parent_uid': parent['uid']})
    assert not device_keys.find_one({'uid': 'test_child_device_uid'})
    assert not lost_children.find_one(
        {'major': child_major, 'minor': child_minor})
    assert not children.find_one({'parent_uid': parent['uid']})


def test_cleanup_users(baseurl):
    global parent_token, child_token
    url = baseurl+'/auth/delete_account'
    res = requests.post(url, json={
        'token': parent_token,
        'password': 'password',
        'confirmPassword': 'password'
    })
    assert res.status_code == 200
    assert res.json()['done'] == 'success'
    child = users.find_one({'email': child_email})
    res = requests.post(url, json={
        'token': child['token'],
        'password': 'password',
        'confirmPassword': 'password'
    })
    assert res.status_code == 200
    assert res.json()['done'] == 'success'
    assert not users.find_one({'email': parent_email})
    assert not users.find_one({'email': child_email})
    client.close()
