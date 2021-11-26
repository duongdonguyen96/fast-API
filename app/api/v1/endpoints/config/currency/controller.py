from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.currency.repository import repos_get_currency


class CtrConfigCurrency(BaseController):
    async def ctr_currency_info(self):
        currency_info = self.call_repos(await repos_get_currency(self.oracle_session))
        return self.response(currency_info)
