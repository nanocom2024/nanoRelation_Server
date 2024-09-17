from DB import DB

db = DB()
children = db.children


def add_child(parent_uid: str, child_uid: str) -> None:
    """
    子どもをDBに追加する

    :param str parent_uid:
    :param str child_uid:
    """
    children.update_one({'parent_uid': parent_uid}, {
                        '$push': {'children': child_uid}}, upsert=True)
