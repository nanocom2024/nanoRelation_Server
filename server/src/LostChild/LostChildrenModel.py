from DB import DB

db = DB()
lost_children = db.lost_children


def add_lost(major: str, minor: str) -> None:
    """
    迷子デバイスのmajorとminorをDBに追加する

    :param str major:
    :param str minor:
    """
    lost_children.insert_one({'major': major, 'minor': minor})


def delete_lost(major: str, minor: str) -> None:
    """
    迷子デバイスのmajorとminorをDBから削除する

    :param str major:
    :param str minor:
    """
    lost_children.delete_many({'major': major, 'minor': minor})


def is_lost_child(major: str, minor: str) -> bool:
    """
    majorとminorがlost_childrenに存在するかどうか

    :param str major:
    :param str minor:
    :return: bool
    """
    return bool(lost_children.find_one({'major': major, 'minor': minor}))
