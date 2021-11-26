from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.staff.repository import (
    repos_get_indirect_sale_staff, repos_get_position, repos_get_sale_staff,
    repos_get_staff_type
)


class CtrConfigStaff(BaseController):
    async def ctr_staff_type_info(self):
        staff_type_info = self.call_repos(await repos_get_staff_type(self.oracle_session))
        return self.response(staff_type_info)

    async def ctr_position_info(self):
        position_info = self.call_repos(await repos_get_position(self.oracle_session))
        return self.response(position_info)

    async def ctr_sale_staff_info(self):
        sale_staff_info = self.call_repos(await repos_get_sale_staff(self.oracle_session))
        return self.response(sale_staff_info)

    async def ctr_indirect_sale_staff_info(self):
        indirect_sale_staff_info = self.call_repos(await repos_get_indirect_sale_staff(self.oracle_session))
        return self.response(indirect_sale_staff_info)
