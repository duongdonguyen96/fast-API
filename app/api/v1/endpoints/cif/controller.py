from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.repository import repos_get_cif_info


class CtrCustomer(BaseController):
    async def ctr_cif_info(self, cif_id: str):
        cif_info = self.call_repos(await repos_get_cif_info(cif_id))
        return self.response(cif_info)
