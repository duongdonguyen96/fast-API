from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.identity_document.repository import (
    repos_get_identity_document, repos_get_sub_identity_document
)


class CtrConfigIdentityDocument(BaseController):
    async def ctr_identity_type_info(self):
        identity_type_info = self.call_repos(await repos_get_identity_document(self.oracle_session))
        return self.response(identity_type_info)

    async def ctr_sub_identity_type_info(self):
        sub_identity_type_info = self.call_repos(await repos_get_sub_identity_document(self.oracle_session))
        return self.response(sub_identity_type_info)
