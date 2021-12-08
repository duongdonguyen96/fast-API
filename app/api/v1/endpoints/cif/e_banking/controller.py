from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.e_banking.repository import (
    repos_balance_saving_account_data, repos_get_detail_reset_password,
    repos_get_detail_reset_password_teller, repos_get_e_banking_data,
    repos_get_list_balance_payment_account, repos_save_e_banking_data
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
        payment_account_data = self.call_repos(
            await repos_get_list_balance_payment_account(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )

        return self.response(data=payment_account_data)

    async def get_detail_reset_password(self, cif_id: str):
        detail_reset_password_data = self.call_repos(await repos_get_detail_reset_password(cif_id))

        return self.response(data=detail_reset_password_data)

    async def ctr_balance_saving_account(self, cif_id: str):
        balance_saving_account_data = self.call_repos(await repos_balance_saving_account_data(cif_id))

        return self.response_paging(
            data=balance_saving_account_data,
            total_item=len(balance_saving_account_data)
        )

    async def get_detail_reset_password_teller(self, cif_id: str):
        detail_reset_password_data = self.call_repos(await repos_get_detail_reset_password_teller(cif_id))

        return self.response(data=detail_reset_password_data)
