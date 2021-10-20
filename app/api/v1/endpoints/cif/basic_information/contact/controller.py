from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.contact.repository import (
    repos_get_detail_contact_information, repos_save_contact_information
)
from app.api.v1.endpoints.cif.basic_information.contact.schema import (
    ContactInformationSaveRequest
)


class CtrContactInformation(BaseController):
    async def detail_contact_information(self, cif_id: str):
        contact_information_detail_data = self.call_repos(
            await repos_get_detail_contact_information(cif_id=cif_id)
        )
        return self.response(data=contact_information_detail_data)

    async def save_contact_information(
            self, cif_id: str,
            contact_information_save_request: ContactInformationSaveRequest
    ):
        contact_information_detail_data = self.call_repos(
            await repos_save_contact_information(
                cif_id=cif_id,
                contact_information_save_request=contact_information_save_request,
                created_by=self.current_user.full_name_vn
            )
        )
        return self.response(data=contact_information_detail_data)
