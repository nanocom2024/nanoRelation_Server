from DB import DB

db = DB()
notification_config = db.notification_config


def enable(req_user, target_user):
    if data := notification_config.find_one({'owner': req_user['uid']}):
        if target_user['uid'] in data['disables']:
            notification_config.update_one(
                {'owner': req_user['uid']},
                {'$pull': {'disables': target_user['uid']}}
            )


def disable(req_user, target_user):
    if data := notification_config.find_one({'owner': req_user['uid']}):
        if not (target_user['uid'] in data['disables']):
            notification_config.update_one(
                {'owner': req_user['uid']},
                {'$push': {'disables': target_user['uid']}}
            )
    else:
        notification_config.insert_one({
            'owner': req_user['uid'],
            'disables': [target_user['uid']]
        })
