from app.api.base.base import Controller
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.repository import (
    repos_get_data_finger
)


class CtrDocument(Controller):
    async def ctr_document(self):
        is_found, document_data = await repos_get_data_finger()
        if not is_found:
            return self.response_exception(msg=document_data)
        return self.response(data=document_data)
