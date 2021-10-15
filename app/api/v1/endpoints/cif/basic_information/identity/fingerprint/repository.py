from typing import Any, Union

from app.api.base.repository import ReposReturn


async def repos_fingerprint(finger_req) -> (bool, Union[str, Any]):
    data = finger_req  # noqa
    return ReposReturn(data=data)
