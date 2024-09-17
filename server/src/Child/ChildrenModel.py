from DB import DB

db = DB()
children = db.children


def add_child(parent_uid: str, child_uid: str) -> None:
    """
    子どもをDBに追加する

    :param parent_uid: str
    :param child_uid: str
    """
    children.update_one({'parent_uid': parent_uid}, {
                        '$push': {'children': child_uid}}, upsert=True)
