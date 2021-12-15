from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.contact.repository import (
    repos_get_detail_contact_information, repos_save_contact_information
)
from app.api.v1.endpoints.cif.basic_information.contact.schema import (
    ContactInformationSaveRequest
)
from app.api.v1.endpoints.cif.repository import repos_get_customer_identity
from app.utils.constant.cif import IDENTITY_DOCUMENT_TYPE_PASSPORT


class CtrContactInformation(BaseController):
    async def detail_contact_information(self, cif_id: str):
        resident_address_active_flag = False
        contact_address_active_flag = False
        last_customer_identity = self.call_repos(await repos_get_customer_identity(
            cif_id=cif_id,
            session=self.oracle_session
        ))
        if last_customer_identity.identity_type_id == IDENTITY_DOCUMENT_TYPE_PASSPORT:
            resident_address_active_flag = True
            contact_address_active_flag = True

        contact_information_detail_data = self.call_repos(
            await repos_get_detail_contact_information(
                cif_id=cif_id,
                resident_address_active_flag=resident_address_active_flag,
                contact_address_active_flag=contact_address_active_flag,
                session=self.oracle_session
            )
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
