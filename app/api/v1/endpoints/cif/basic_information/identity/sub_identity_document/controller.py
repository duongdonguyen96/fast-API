from typing import List

from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.sub_identity_document.repository import (
    repos_get_detail, repos_get_list_log, repos_save
)
from app.api.v1.endpoints.cif.basic_information.identity.sub_identity_document.schema import (
    SubIdentityDocumentRequest
)
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST


class CtrSubIdentityDocument(BaseController):
    async def get_detail(self, cif_id: str):
        detail_data = self.call_repos(
            await repos_get_detail(
                cif_id=cif_id
            )
        )
        return self.response(data=detail_data)

    async def get_list_log(self, cif_id: str):
        logs_data = self.call_repos(
            await repos_get_list_log(cif_id=cif_id)
        )
        return self.response(data=logs_data)

    async def save(
            self, cif_id: str,
            requests: List[SubIdentityDocumentRequest]
    ):
        if cif_id is None or cif_id != CIF_ID_TEST:
            return self.response_exception(loc="cif_id", msg=ERROR_CIF_ID_NOT_EXIST)

        info_save_document = self.call_repos(
            await repos_save(
                cif_id,
                requests=requests,
                created_by=self.current_user.full_name_vn
            )
        )
        return self.response(data=info_save_document)
