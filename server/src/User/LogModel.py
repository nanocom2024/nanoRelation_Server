from User.LogOwnModel import get_log_own
from User.LogNearOwnChildrenModel import get_log_near_own_children
from User.LogLostPassesModel import get_log_lost_passes
from User.LogPassesModel import get_log_passes
from Child.ChildrenModel import is_registered_child


def get_logs(request_uid: str, target_uid: str) -> list:
    """
    ログを取得する(order by timestamp)

    :param str request_uid:
    :param str target_uid:
    :return list:
    """
    if request_uid == target_uid:

        # tag -> own
        return get_log_own(owner_uid=request_uid)

    elif is_registered_child(parent_uid=request_uid, child_uid=target_uid):
        logs = get_log_near_own_children(
            parent_uid=request_uid, child_uid=target_uid)
        # logs.extend(get_log_lost_passes(
        #     owner_uid=request_uid, child_uid=target_uid))

        # tag -> child or lost
        return sorted(logs, key=lambda x: x['timestamp'])

    else:
        logs = get_log_passes(request_uid=request_uid, target_uid=target_uid)
        # logs.extend(get_log_lost_passes(
        #     owner_uid=request_uid, child_uid=target_uid))

        # tag -> pass or lost
        return sorted(logs, key=lambda x: x['timestamp'])
