from DB import DB
from datetime import datetime, timedelta


# MongoDBに接続
db = DB()


def add_log_near_own_children(parent_uid: str, child_uid: str) -> None:
    """
    自身の子供のデバイスを検知したログを保存する

    30秒間に一回保存する

    :param str owner_uid:
    :param str child_uid:
    """
    current_time = datetime.now()

    # owner_uid に対する最新のログを取得
    log_latest = db.log_near_own_children.find_one(
        {'parent_uid': parent_uid, 'child_uid': child_uid})

    # ログが存在するか、または最新のログが30秒以内かを確認
    if log_latest:
        last_timestamp = log_latest['timestamps'][-1]  # 最後に保存したタイムスタンプ
        last_log_time = datetime.fromtimestamp(last_timestamp)
        time_difference = current_time - last_log_time

        # 最新のログが30秒以内なら保存しない
        if time_difference <= timedelta(seconds=30):
            return

    # ログがない、または30秒以上経過している場合は保存
    db.log_near_own_children.update_one(
        {'parent_uid': parent_uid, 'child_uid': child_uid},
        {'$push': {'timestamps': current_time.timestamp()}},
        upsert=True
    )


def get_log_near_own_children(parent_uid: str, child_uid: str) -> list:
    """
    自身の子供のデバイスを検知したログを取得する(order by timestamp)

    :param str owner_uid:
    :param str child_uid:
    :return: list
    """
    log_near_own_children = db.log_near_own_children.find_one(
        {'parent_uid': parent_uid, 'child_uid': child_uid})
    if not log_near_own_children:
        return []

    res = [{'tag': 'child', 'timestamp': timestamp}
           for timestamp in log_near_own_children['timestamps']]
    return res
