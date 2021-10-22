from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.profile_history.repository import (
    repos_profile_history
)


class CtrProfileHistory(BaseController):
    async def ctr_profile_history(self, cif_id: str):
        profile_history = self.call_repos((await repos_profile_history(cif_id)))
        return self.response(profile_history)
