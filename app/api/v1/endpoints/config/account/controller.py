from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.account import (
    AccountClass, AccountType
)


class CtrConfigAccount(BaseController):
    async def ctr_account_type_info(self):
        account_type_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session, model=AccountType
            )
        )
        return self.response(account_type_info)

    async def ctr_account_class_info(self):
        account_class_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session, model=AccountClass
            )
        )
        return self.response(account_class_info)
