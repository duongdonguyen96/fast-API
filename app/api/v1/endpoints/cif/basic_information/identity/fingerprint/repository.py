from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.fake_data import (
    FINGERPRINT_DATA
)


async def repos_get_data_finger() -> ReposReturn:
    return ReposReturn(data=FINGERPRINT_DATA)
