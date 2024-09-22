from datetime import datetime
from DB import DB

db = DB()
log_lost_children = db.log_lost_children


def add_log_lost(child_uid: str, msgID: str, text: str, tag: str, timestamp: datetime) -> None:
    """
    迷子デバイスのmajorとminorをDBに追加する

    :param str child_uid:
    :param str msgID:
    :param str text:
    :param datetime timestamp:
    """
    log_lost_children.update_one({'child_uid': child_uid}, {
        '$push': {'messages': {'msgID': msgID, 'text': text, 'tag': tag, 'timestamp': timestamp}}}, upsert=True)
