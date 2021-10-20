from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.fatca.repository import (
    repos_get_fatca_data
)


class CtrFatca(BaseController):
    async def ctr_get_fatca(self, cif_id: str):
        fatca_data = self.call_repos(await repos_get_fatca_data(cif_id))

        return self.response(data=fatca_data)
