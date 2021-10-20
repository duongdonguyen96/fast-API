from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.guardian.repository import (
    repos_detail_guadian
)


class CtrGuardian(BaseController):
    async def detail(self, cif_id: str):
        guardian_info = self.call_repos(await repos_detail_guadian(cif_id=cif_id))
        return self.response(data=guardian_info)
