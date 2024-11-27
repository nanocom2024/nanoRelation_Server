from DB import DB
from datetime import datetime, timedelta


# MongoDBに接続
db = DB()


def add_log_lost_passes(provider_uid: str, parent_uid: str, latitude: float = 0, longitude: float = 0) -> None:
    """
    迷子になったデバイスを検知したログを保存する

    :param str provider_uid: デバイスを検知したユーザーのUID
    :param str parent_uid: 迷子になったデバイスの親デバイスのUID
    :param float latitude: default 0
    :param float longitude: default 0
    """
    current_time = datetime.now()

    db.log_lost_passes.update_one(
        {'provider_uid': provider_uid, 'parent_uid': parent_uid},
        {'$push': {'timestamps': {
            'timestamp': current_time.timestamp(),
            'latitude': latitude,
            'longitude': longitude
        }}},
        upsert=True
    )


def get_log_lost_passes(parent_uid: str) -> list:
    """
    迷子になったデバイスを検知したログを取得する(order by timestamp)

    :param str parent_uid:
    :return: list
    """
    log_lost_passes = db.log_lost_passes.find_one({'parent_uid': parent_uid})
    if not log_lost_passes:
        return []

    res = log_lost_passes['timestamps']
    return res
