from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.other_information.repository import (
    repos_other_info, repos_update_other_info
)
from app.api.v1.endpoints.cif.other_information.schema import (
    OtherInformationUpdateRequest
)


class CtrOtherInfo(BaseController):
    async def ctr_other_info(self, cif_id: str):
        other_information = self.call_repos(await repos_other_info(cif_id, self.oracle_session))
        return self.response(other_information)

    async def ctr_update_other_info(self, cif_id: str, update_other_info_req: OtherInformationUpdateRequest):
        update_other_info = self.call_repos(await repos_update_other_info(cif_id, update_other_info_req))
        return self.response(update_other_info)
