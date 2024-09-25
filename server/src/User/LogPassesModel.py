from DB import DB


# MongoDBに接続
db = DB()


def get_log_passes(request_uid: str, target_uid: str) -> list:
    """
    すれ違いのログを取得する(unordered)

    :param str request_uid:
    :param str target_uid:
    :return list:
    """
    uid1 = min(request_uid, target_uid)
    uid2 = max(request_uid, target_uid)
    log_passes = db.log_passes.find({'uid1': uid1, 'uid2': uid2})
    if not log_passes:
        return []

    res = [{'tag': 'pass', 'timestamp': log['timestamp']}
           for log in log_passes]

    return res
