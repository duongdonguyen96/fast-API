from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.repository import (
    repos_fingerprint
)
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.schema import (
    FingerReq
)


class CtrFingerPrint(BaseController):
    async def ctr_save_fingerprint(self, finger_req: FingerReq):
        is_false, data = await repos_fingerprint(finger_req)
        return self.response(data=data)
