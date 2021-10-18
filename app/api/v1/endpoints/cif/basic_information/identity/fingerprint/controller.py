from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.repository import (
    repos_fingerprint, repos_get_data_finger
)
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.schema import (
    FingerRequest
)


class CtrFingerPrint(BaseController):
    async def ctr_save_fingerprint(self, finger_request: FingerRequest):
        data = self.call_repos(await repos_fingerprint(finger_request))
        return self.response(data=data)

    async def ctr_get_fingerprint(self, cif_id: str):
        fingerprint_data = self.call_repos(await repos_get_data_finger(cif_id))
        return self.response(data=fingerprint_data)
