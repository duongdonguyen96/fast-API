from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.repository import (
    repos_get_data_finger
)


class CtrFingerPrint(BaseController):
    async def ctr_get_fingerprint(self):
        fingerprint_data = self.call_repos(await repos_get_data_finger())
        return self.response(data=fingerprint_data)
