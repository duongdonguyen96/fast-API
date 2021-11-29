from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.staff.repository import (
    repos_get_indirect_sale_staff, repos_get_sale_staff
)
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.others import (
    Position, StaffType
)


class CtrConfigStaff(BaseController):
    async def ctr_staff_type_info(self):
        staff_type_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=StaffType,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(staff_type_info)

    async def ctr_position_info(self):
        position_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=Position,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(position_info)

    async def ctr_sale_staff_info(self):
        sale_staff_info = self.call_repos(await repos_get_sale_staff(self.oracle_session))
        return self.response(sale_staff_info)

    async def ctr_indirect_sale_staff_info(self):
        indirect_sale_staff_info = self.call_repos(await repos_get_indirect_sale_staff(self.oracle_session))
        return self.response(indirect_sale_staff_info)
