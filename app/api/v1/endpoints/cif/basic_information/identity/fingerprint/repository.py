from typing import Any, Union


async def repos_fingerprint(finger_req) -> (bool, Union[str, Any]):
    data = finger_req  # noqa
    return True, "message thành công"
