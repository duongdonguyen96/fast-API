from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.payment_account.co_owner.repository import (
    repos_get_agreement_authorization
)


class CtrConfigCoOwner(BaseController):
    async def ctr_agreement_info(self):
        agreement_info = self.call_repos(await repos_get_agreement_authorization(session=self.oracle_session))
        return self.response(agreement_info)
