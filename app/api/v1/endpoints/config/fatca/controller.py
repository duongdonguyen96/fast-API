from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.others import FatcaCategory


class CtrConfigFatca(BaseController):
    async def ctr_fatca_info(self):
        fatca_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=FatcaCategory
            )
        )
        return self.response(fatca_info)
