from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.repository import \
    repos_get_detail_identity_document, repos_save_identity_document
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.schema import IdentityCardReqRes, \
    CitizenCardReqRes, PassportDocumentReqRes


class CtrIdentity(BaseController):
    async def detail_identity_document(self, cif_id: str):
        identity_card_detail_data = self.call_repos(
            await repos_get_detail_identity_document(cif_id)
        )
        return self.response(data=identity_card_detail_data)

    async def save_identity_card(self, identity_card_document_req: IdentityCardReqRes):
        info_identity_document = self.call_repos(
            await repos_save_identity_document(identity_card_document_req, self.current_user.full_name)
        )
        return self.response(data=info_identity_document)

    async def save_citizen_card(self, citizen_card_document_req: CitizenCardReqRes):
        info_identity_document = self.call_repos(
            await repos_save_identity_document(citizen_card_document_req, self.current_user.full_name)
        )
        return self.response(data=info_identity_document)

    async def save_passport(self, passport_document_req: PassportDocumentReqRes):
        info_identity_document = self.call_repos(
            await repos_save_identity_document(passport_document_req, self.current_user.full_name)
        )
        return self.response(data=info_identity_document)
