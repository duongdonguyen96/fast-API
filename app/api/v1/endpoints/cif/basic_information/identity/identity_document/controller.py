from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.repository import (
    repos_get_detail_identity_document, repos_save_identity_document
)


class CtrIdentityDocument(BaseController):
    async def detail_identity_document(self, cif_id: str, identity_document_type_code: str):
        identity_card_detail_data = self.call_repos(
            await repos_get_detail_identity_document(
                cif_id=cif_id,
                identity_document_type_code=identity_document_type_code
            )
        )
        return self.response(data=identity_card_detail_data)

    async def save_identity_document(self, identity_document_req):
        # trong body có truyền cif_id khác None thì lưu lại, truyền bằng None thì sẽ là tạo mới
        if identity_document_req.cif_id is None:
            identity_document_req.cif_id = "NEW123"

        info_save_document = self.call_repos(
            await repos_save_identity_document(
                identity_card_document_req=identity_document_req,
                created_by=self.current_user.full_name_vn
            )
        )
        return self.response(data=info_save_document)
