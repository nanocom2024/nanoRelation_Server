from DB import DB
from datetime import datetime, timedelta


# MongoDBに接続
db = DB()


def add_log_own(owner_uid: str) -> None:
    """
    自身のデバイスを検知したログを保存する

    一分間に一回保存する

    :param str owner_uid:
    """
    current_time = datetime.now()

    # owner_uid に対する最新のログを取得
    log_latest = db.log_own.find_one({'owner_uid': owner_uid})

    # ログが存在するか、または最新のログが1分以内かを確認
    if log_latest:
        last_timestamp = log_latest['timestamps'][-1]  # 最後に保存したタイムスタンプ
        last_log_time = datetime.fromtimestamp(last_timestamp)
        time_difference = current_time - last_log_time

        # 最新のログが1分以内なら保存しない
        if time_difference <= timedelta(minutes=1):
            return

    # ログがない、または1分以上経過している場合は保存
    db.log_own.update_one(
        {'owner_uid': owner_uid},
        {'$push': {'timestamps': current_time.timestamp()}},
        upsert=True
    )


def get_log_own(owner_uid: str) -> list:
    """
    自身のデバイスを検知したログを取得する(order by timestamp)

    :param str owner_uid:
    :return: list
    """
    log_own = db.log_own.find_one({'owner_uid': owner_uid})
    if not log_own:
        return []

    res = [{'tag': 'own', 'timestamp': timestamp}
           for timestamp in log_own['timestamps']]
    return res
