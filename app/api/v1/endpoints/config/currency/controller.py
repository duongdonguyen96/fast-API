from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.others import Currency


class CtrConfigCurrency(BaseController):
    async def ctr_currency_info(self):
        currency_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=Currency,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(currency_info)
