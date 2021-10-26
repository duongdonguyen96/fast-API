from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.e_banking.repository import (
    repos_get_e_banking_data, repos_get_list_balance_payment_account,
    repos_save_e_banking_data
)
from app.api.v1.endpoints.cif.e_banking.schema import EBankingRequest


class CtrEBanking(BaseController):
    async def ctr_save_e_banking(self, cif_id: str, e_banking: EBankingRequest):
        e_banking_data = self.call_repos(
            await repos_save_e_banking_data(
                cif_id,
                e_banking,
                created_by=self.current_user.full_name_vn
            )
        )

        return self.response(data=e_banking_data)

    async def ctr_e_banking(self, cif_id: str):
        e_banking_data = self.call_repos(await repos_get_e_banking_data(cif_id))

        return self.response(data=e_banking_data)

    async def ctr_balance_payment_account(self, cif_id: str):
        payment_account_data = self.call_repos(await repos_get_list_balance_payment_account(cif_id))

        return self.response(data=payment_account_data)
