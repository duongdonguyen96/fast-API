from typing import Any, Union

from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.fake_data import (
    FINGERPRINT_DATA
)


async def repos_get_data_finger() -> (bool, Union[str, Any]):
    return True, FINGERPRINT_DATA
