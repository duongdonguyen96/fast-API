from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.sub_identity_document.repository import \
    repos_get_detail_sub_identity_document


class CtrSubIdentityDocument(BaseController):
    async def detail_sub_identity_document(self, cif_id: str):
        sub_identity_card_detail_data = self.call_repos(
            await repos_get_detail_sub_identity_document(
                cif_id=cif_id
            )
        )
        return self.response(data=sub_identity_card_detail_data)
