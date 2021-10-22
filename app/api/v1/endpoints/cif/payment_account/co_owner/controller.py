from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.payment_account.co_owner.repository import (
    repos_get_co_owner_data
)


class CtrCoOwner(BaseController):
    async def ctr_co_owner(self, cif_id: str):
        co_owner_data = self.call_repos(await repos_get_co_owner_data(cif_id))

        return self.response(data=co_owner_data)
