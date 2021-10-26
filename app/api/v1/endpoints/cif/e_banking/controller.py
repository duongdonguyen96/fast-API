from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.e_banking.repository import (
    repos_get_detail_reset_password, repos_get_e_banking_data,
    repos_get_list_balance_payment_account
)


class CtrEBanking(BaseController):
    async def ctr_e_banking(self, cif_id: str):
        e_banking_data = self.call_repos(await repos_get_e_banking_data(cif_id))

        return self.response(data=e_banking_data)

    async def ctr_balance_payment_account(self, cif_id: str):
        payment_account_data = self.call_repos(await repos_get_list_balance_payment_account(cif_id))

        return self.response(data=payment_account_data)

    async def get_detail_reset_password(self, cif_id: str):
        detail_reset_password_data = self.call_repos(await repos_get_detail_reset_password(cif_id))

        return self.response(data=detail_reset_password_data)
