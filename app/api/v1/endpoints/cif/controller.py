from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.repository import (
    repos_get_cif_info, repos_profile_history
)


class CtrCustomer(BaseController):
    async def ctr_cif_info(self, cif_id: str):
        cif_info = self.call_repos(await repos_get_cif_info(cif_id))
        return self.response(cif_info)

    async def ctr_profile_history(self, cif_id: str):
        profile_history = self.call_repos((await repos_profile_history(cif_id)))
        return self.response(profile_history)
