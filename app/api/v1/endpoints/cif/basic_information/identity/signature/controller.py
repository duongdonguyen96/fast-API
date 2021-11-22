from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.signature.repository import (
    repos_get_identity_id, repos_get_signature_data, repos_get_type_id,
    repos_save_signature
)
from app.api.v1.endpoints.cif.basic_information.identity.signature.schema import (
    SignaturesRequest
)
from app.utils.functions import now


class CtrSignature(BaseController):
    async def ctr_save_signature(self, cif_id: str, signatures: SignaturesRequest):

        type_id = self.call_repos(await repos_get_type_id(self.oracle_session))
        identity = self.call_repos(await repos_get_identity_id(cif_id, self.oracle_session))

        list_data_insert = [{
            'identity_id': identity.id,
            'image_type_id': type_id.code,
            'image_url': signature.image_url,
            'hand_side_id': None,
            'finger_type_id': None,
            'vector_data': None,
            'active_flag': 1,
            'maker_id': self.current_user.user_id,
            'maker_at': now(),
            'identity_image_front_flag': None
        } for signature in signatures.signatures]

        data = self.call_repos(
            await repos_save_signature(
                cif_id,
                list_data_insert,
                self.oracle_session,
                created_by=self.current_user.full_name_vn
            )
        )

        return self.response(data=data)

    async def ctr_get_signature(self, cif_id: str):
        signature_data = self.call_repos(await repos_get_signature_data(cif_id))

        return self.response(data=signature_data)
