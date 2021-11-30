from typing import List

from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.sub_identity_document.repository import (
    repos_get_detail, repos_get_list_log, repos_save_sub_identity
)
from app.api.v1.endpoints.cif.basic_information.identity.sub_identity_document.schema import (
    SubIdentityDocumentRequest
)
from app.api.v1.endpoints.cif.basic_information.repository import (
    repos_get_identity_document_types, repos_get_place_of_issue
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer


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

    async def save_sub_identity(
            self, cif_id: str,
            sub_identity_requests: List[SubIdentityDocumentRequest]
    ):
        # check cif đang tạo
        customer = self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))
        sub_identity_type_ids = []
        place_of_issue_ids = []
        for sub_identity in sub_identity_requests:
            sub_identity_type_ids.append(sub_identity.sub_identity_document_type.id)
            place_of_issue_ids.append(sub_identity.ocr_result.place_of_issue.id)

        # check exits sub_identity_type_ids
        self.call_repos(await repos_get_identity_document_types(sub_identity_type_ids=sub_identity_type_ids,
                                                                session=self.oracle_session))
        self.call_repos(
            await repos_get_place_of_issue(place_of_issue_ids=set(place_of_issue_ids), session=self.oracle_session))

        info_save_document = self.call_repos(
            await repos_save_sub_identity(
                customer=customer,
                sub_identity_requests=sub_identity_requests,
                saved_by=self.current_user.full_name_vn,
                session=self.oracle_session
            )
        )
        return self.response(data=info_save_document)
