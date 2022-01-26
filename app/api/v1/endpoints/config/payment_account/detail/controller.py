from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.payment_account.detail.repository import (
    repos_get_account_structure_type
)


class CtrConfigPaymentDetail(BaseController):
    async def ctr_account_structure_type_info(self, level: int):
        account_structure_type_infos = self.call_repos(
            await repos_get_account_structure_type(
                level=level,
                session=self.oracle_session
            )
        )

        return self.response(account_structure_type_infos)
