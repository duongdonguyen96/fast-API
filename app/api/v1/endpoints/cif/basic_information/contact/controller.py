from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.contact.repository import (
    repos_get_detail_contact_information
)


class CtrContactInformation(BaseController):
    async def detail_contact_information(self, cif_id: str):
        contact_information_detail_data = self.call_repos(
            await repos_get_detail_contact_information(cif_id=cif_id)
        )
        return self.response(data=contact_information_detail_data)
