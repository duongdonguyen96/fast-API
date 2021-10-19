from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.personal.repository import (
    repos_get_personal_data
)


class CtrPersonal(BaseController):
    async def ctr_personal(self, cif_id: str):
        personal_data = self.call_repos(await repos_get_personal_data(cif_id))

        return self.response(data=personal_data)
