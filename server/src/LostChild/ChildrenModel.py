from DB import DB

db = DB()
children = db.children


def is_registered_child(parent_uid: str, child_uid: str) -> bool:
    """
    子どもが登録されているか確認する

    :param parent_uid: str
    :param child_uid: str
    :return: bool
    """
    return bool(children.find_one({'parent_uid': parent_uid, 'children': child_uid}))
