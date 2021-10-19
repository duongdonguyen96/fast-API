from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.signature.repository import (
    repos_get_signature_data, repos_save_signature
)
from app.api.v1.endpoints.cif.basic_information.identity.signature.schema import (
    SignaturesRequest
)


class CtrSignature(BaseController):
    async def ctr_save_signature(self, cif_id: str, signature: SignaturesRequest):
        data = self.call_repos(
            await repos_save_signature(
                cif_id,
                signature,
                created_by=self.current_user.full_name_vn
            )
        )

        return self.response(data=data)

    async def ctr_get_signature(self, cif_id: str):
        signature_data = self.call_repos(await repos_get_signature_data(cif_id))

        return self.response(data=signature_data)
