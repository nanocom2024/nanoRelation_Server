from DB import DB
from datetime import datetime, timedelta


# MongoDBに接続
db = DB()


def add_log_lost_passes(owner_uid: str, child_uid: str, latitude: float = 0, longitude: float = 0) -> None:
    """
    迷子になったデバイスを検知したログを保存する

    30秒間に一回保存する

    :param str owner_uid:
    :param str child_uid:
    :param float latitude: default 0
    :param float longitude: default 0
    """
    current_time = datetime.now()

    # owner_uid に対する最新のログを取得
    log_latest = db.log_lost_passes.find_one(
        {'owner_uid': owner_uid, 'child_uid': child_uid})

    # ログが存在するか、または最新のログが30秒以内かを確認
    if log_latest:
        # 最後に保存したタイムスタンプ
        last_timestamp = log_latest['timestamps'][-1]['timestamp']
        last_log_time = datetime.fromtimestamp(last_timestamp)
        time_difference = current_time - last_log_time

        # 最新のログが30秒以内なら保存しない
        if time_difference <= timedelta(seconds=30):
            return

    # ログがない、または30秒以上経過している場合は保存
    db.log_lost_passes.update_one(
        {'owner_uid': owner_uid, 'child_uid': child_uid},
        {'$push': {'timestamps': {
            'timestamp': current_time.timestamp(),
            'latitude': latitude,
            'longitude': longitude
        }}},
        upsert=True
    )


def get_log_lost_passes(owner_uid: str, child_uid: str) -> list:
    """
    迷子になったデバイスを検知したログを取得する(order by timestamp)

    :param str owner_uid:
    :param str child_uid:
    :return: list
    """
    log_lost_passes = db.log_lost_passes.find_one(
        {'owner_uid': owner_uid, 'child_uid': child_uid})
    if not log_lost_passes:
        return []

    res = [{'tag': 'lost', 'timestamp': one_pass['timestamp']}
           for one_pass in log_lost_passes['timestamps']]
    return res
