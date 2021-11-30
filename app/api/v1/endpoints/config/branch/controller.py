from typing import Optional

from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.branch.repository import repos_get_branch


class CtrBranch(BaseController):
    async def ctr_branch_info(self, region_id: Optional[str]):
        branches_info = self.call_repos(
            await repos_get_branch(session=self.oracle_session, region_id=region_id)
        )
        return self.response(branches_info)
