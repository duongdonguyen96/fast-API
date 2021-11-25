from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.staff.repository import (
    repos_get_position, repos_get_staff_type
)


class CtrConfigStaff(BaseController):
    async def ctr_staff_type_info(self):
        staff_type_info = self.call_repos(await repos_get_staff_type(self.oracle_session))
        return self.response(staff_type_info)

    async def ctr_position_info(self):
        position_info = self.call_repos(await repos_get_position(self.oracle_session))
        return self.response(position_info)
