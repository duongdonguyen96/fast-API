from typing import Optional

from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.account import (
    AccountStructureType
)


class CtrConfigPaymentDetail(BaseController):
    async def ctr_account_structure_type_info(
            self,
            level: Optional[int],
            parent_id: str
    ):
        account_structure_type_infos = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=AccountStructureType,
                parent_id=parent_id,
                level=level
            )
            # await repos_get_account_structure_type(
            #     level=level,
            #     parent_id=parent_id,
            #     session=self.oracle_session
            # )
        )

        return self.response(account_structure_type_infos)
