from typing import Any, Union

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.fake_data import (
    FINGERPRINT_DATA
)


async def repos_fingerprint(finger_req) -> (bool, Union[str, Any]):
    data = finger_req  # noqa
    return ReposReturn(data=data)


async def repos_get_data_finger(cif_id: str) -> ReposReturn:
    return ReposReturn(data=FINGERPRINT_DATA)
