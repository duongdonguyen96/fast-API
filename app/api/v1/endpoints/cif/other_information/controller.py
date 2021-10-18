from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.other_information.repository import (
    repo_other_info
)


class CtrOtherInfo(BaseController):
    async def ctr_other_info(self, cif_id: str):
        other_information = self.call_repos(await repo_other_info(cif_id))
        return self.response(other_information)
