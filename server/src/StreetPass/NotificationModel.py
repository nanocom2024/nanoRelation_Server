from DB import DB

db = DB()
notification_config = db.notification_config


def check_notification_allowed(req_user, target_user):
    if data := notification_config.find_one({'owner': req_user['uid']}):
        if target_user['uid'] in data['disables']:
            return False
    if data := notification_config.find_one({'owner': target_user['uid']}):
        if req_user['uid'] in data['disables']:
            return False
    return True
