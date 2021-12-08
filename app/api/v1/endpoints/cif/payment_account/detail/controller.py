from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.payment_account.detail.repository import (
    repos_detail_payment_account, repos_save_payment_account
)
from app.api.v1.endpoints.cif.payment_account.detail.schema import (
    SavePaymentAccountRequest
)


class CtrPaymentAccount(BaseController):
    async def detail(self, cif_id: str):
        detail_payment_account_info = self.call_repos(
            await repos_detail_payment_account(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )
        return self.response(detail_payment_account_info)

    async def save(self, cif_id, payment_account_save_request: SavePaymentAccountRequest):
        save_payment_account_info = self.call_repos(await repos_save_payment_account(
            cif_id=cif_id,
            payment_account_save_request=payment_account_save_request,
            created_by=self.current_user.full_name_vn
        ))
        return self.response(data=save_payment_account_info)
