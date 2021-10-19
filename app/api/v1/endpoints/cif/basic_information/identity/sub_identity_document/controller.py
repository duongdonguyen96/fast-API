from typing import List

from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.sub_identity_document.repository import \
    repos_get_detail_sub_identity_document, repos_save_sub_identity_document
from app.api.v1.endpoints.cif.basic_information.identity.sub_identity_document.schema import SubIdentityDocumentRequest
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST


class CtrSubIdentityDocument(BaseController):
    async def detail_sub_identity_document(self, cif_id: str):
        sub_identity_card_detail_data = self.call_repos(
            await repos_get_detail_sub_identity_document(
                cif_id=cif_id
            )
        )
        return self.response(data=sub_identity_card_detail_data)

    async def save_sub_identity_document(
            self, cif_id: str,
            sub_identity_document_requests: List[SubIdentityDocumentRequest]
    ):

        if cif_id is None or cif_id != CIF_ID_TEST:
            return self.response_exception(loc="cif_id", msg=ERROR_CIF_ID_NOT_EXIST)

        info_save_document = self.call_repos(
            await repos_save_sub_identity_document(
                cif_id,
                sub_identity_document_requests=sub_identity_document_requests,
                created_by=self.current_user.full_name_vn
            )
        )
        return self.response(data=info_save_document)
