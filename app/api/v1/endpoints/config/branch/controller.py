from typing import Optional

from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.others import Branch


class CtrBranch(BaseController):
    async def ctr_branch_info(
            self, region_id: Optional[str],
            province_id: Optional[str],
            district_id: Optional[str],
            ward_id: Optional[str]
    ):
        branch_info = self.call_repos(
            await repos_get_data_model_config(
                region_id=region_id,
                province_id=province_id,
                district_id=district_id,
                ward_id=ward_id,
                session=self.oracle_session,
                model=Branch
            )
        )
        return self.response(branch_info)
