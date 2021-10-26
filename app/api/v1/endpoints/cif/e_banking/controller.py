from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.e_banking.repository import (
    repos_balance_saving_account_data, repos_get_e_banking_data
)


class CtrEBanking(BaseController):
    async def ctr_e_banking(self, cif_id: str):
        e_banking_data = self.call_repos(await repos_get_e_banking_data(cif_id))

        return self.response(data=e_banking_data)

    async def ctr_balance_saving_account(self, cif_id: str):
        balance_saving_account_data = self.call_repos(await repos_balance_saving_account_data(cif_id))
        return self.response(data=balance_saving_account_data)
