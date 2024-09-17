from DB import DB

db = DB()
lost_children = db.lost_children


def is_lost_child(major: str, minor: str) -> bool:
    """
    majorとminorがlost_childrenに存在するかどうか

    :param str major:
    :param str minor:
    :return: bool
    """
    return bool(lost_children.find_one({'major': major, 'minor': minor}))
