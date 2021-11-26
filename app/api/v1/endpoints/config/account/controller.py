from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.account.repository import (
    repos_get_account_class, repos_get_account_type
)


class CtrConfigAccount(BaseController):
    async def ctr_account_type_info(self):
        account_type_info = self.call_repos(await repos_get_account_type(self.oracle_session))
        return self.response(account_type_info)

    async def ctr_account_class_info(self):
        account_class_info = self.call_repos(await repos_get_account_class(self.oracle_session))
        return self.response(account_class_info)
