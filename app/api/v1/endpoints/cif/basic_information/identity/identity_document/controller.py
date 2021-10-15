from app.api.base.base import Controller
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.repository import \
    repos_get_detail_identity_document


class CtrIdentity(Controller):
    async def detail(self, cif_id: str, identity_document_type: int):
        is_found, identity_document_detail_data = await repos_get_detail_identity_document(cif_id, identity_document_type)
        if not is_found:
            return self.response_exception(msg=identity_document_detail_data, loc="cif_id,")
        return self.response(data=identity_document_detail_data)