from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.fatca.repository import (
    repos_get_fatca_data, repos_save_fatca
)
from app.api.v1.endpoints.cif.basic_information.fatca.schema import (
    FatcaRequest
)


class CtrFatca(BaseController):
    async def ctr_save_fatca(self, cif_id: str, fatca: FatcaRequest):
        fatca_data = self.call_repos(
            await repos_save_fatca(
                cif_id,
                fatca,
                created_by=self.current_user.full_name_vn
            )
        )
        return self.response(data=fatca_data)

    async def ctr_get_fatca(self, cif_id: str):
        fatca_data = self.call_repos(await repos_get_fatca_data(cif_id))

        return self.response(data=fatca_data)
