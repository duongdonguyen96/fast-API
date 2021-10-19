from typing import Union

from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.repository import (
    repos_get_detail_identity_document, repos_save_identity_document
)
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.schema_request import (
    CitizenCardSaveRequest, IdentityCardSaveRequest, PassportSaveRequest
)
from app.utils.constant.cif import CIF_ID_NEW_TEST


class CtrIdentityDocument(BaseController):
    async def detail_identity_document(self, cif_id: str, identity_document_type_id: str):
        identity_card_detail_data = self.call_repos(
            await repos_get_detail_identity_document(
                cif_id=cif_id,
                identity_document_type_id=identity_document_type_id
            )
        )
        return self.response(data=identity_card_detail_data)

    async def save_identity_document(
            self,
            identity_document_req: Union[IdentityCardSaveRequest, CitizenCardSaveRequest, PassportSaveRequest]
    ):
        # trong body có truyền cif_id khác None thì lưu lại, truyền bằng None thì sẽ là tạo mới
        if identity_document_req.cif_id is None:
            identity_document_req.cif_id = "NEW123"

        info_save_document = self.call_repos(
            await repos_save_identity_document(
                identity_document_req=identity_document_req,
                created_by=self.current_user.full_name_vn
            )
        )
        return self.response(data=info_save_document)
