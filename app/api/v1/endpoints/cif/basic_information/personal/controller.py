from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.personal.repository import (
    repos_get_personal_data, repos_save_personal
)
from app.api.v1.endpoints.cif.basic_information.personal.schema import (
    PersonalRequest
)


class CtrPersonal(BaseController):
    async def ctr_save_personal(self, cif_id: str, personal: PersonalRequest):
        personal_data = self.call_repos(
            await repos_save_personal(
                cif_id,
                personal,
                created_by=self.current_user.full_name_vn
            )
        )

        return self.response(data=personal_data)

    async def ctr_personal(self, cif_id: str):
        personal_data = self.call_repos(await repos_get_personal_data(cif_id=cif_id, session=self.oracle_session))

        return self.response(data=personal_data)
