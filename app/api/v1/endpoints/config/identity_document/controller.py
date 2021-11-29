from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.identity import (
    CustomerIdentityType, CustomerSubIdentityType
)


class CtrConfigIdentityDocument(BaseController):
    async def ctr_identity_type_info(self):
        identity_type_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=CustomerIdentityType
            )
        )
        return self.response(identity_type_info)

    async def ctr_sub_identity_type_info(self):
        sub_identity_type_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=CustomerSubIdentityType
            )
        )
        return self.response(sub_identity_type_info)
