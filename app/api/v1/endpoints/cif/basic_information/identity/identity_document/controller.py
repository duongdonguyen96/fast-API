from typing import Union

from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.repository import (
    repos_get_detail, repos_get_list_log, repos_save
)
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.schema_request import (
    CitizenCardSaveRequest, IdentityCardSaveRequest, PassportSaveRequest
)
from app.utils.constant.cif import CIF_ID_NEW_TEST


class CtrIdentityDocument(BaseController):
    async def detail(self, cif_id: str, identity_document_type_id: str):
        detail_data = self.call_repos(
            await repos_get_detail(
                cif_id=cif_id,
                identity_document_type_id=identity_document_type_id,
                oracle_session=self.oracle_session,
                current_user=self.current_user
            )
        )
        return self.response(data=detail_data)

    async def get_list_log(self, cif_id: str):
        logs_data = self.call_repos(
            await repos_get_list_log(cif_id=cif_id)
        )
        return self.response(data=logs_data)

    async def save(
            self,
            identity_document_req: Union[IdentityCardSaveRequest, CitizenCardSaveRequest, PassportSaveRequest]
    ):
        # trong body có truyền cif_id khác None thì lưu lại, truyền bằng None thì sẽ là tạo mới
        if identity_document_req.cif_id is None:
            identity_document_req.cif_id = CIF_ID_NEW_TEST

        info_save_document = self.call_repos(
            await repos_save(
                identity_document_req=identity_document_req,
                created_by=self.current_user.full_name_vn
            )
        )
        return self.response(data=info_save_document)
