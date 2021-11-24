from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.signature.repository import (
    repos_get_signature_data, repos_save_signature
)
from app.api.v1.endpoints.cif.basic_information.identity.signature.schema import (
    SignaturesRequest
)
from app.api.v1.endpoints.cif.repository import (
    repos_get_initializing_customer, repos_get_last_identity
)
from app.utils.constant.cif import (
    ACTIVE_FLAG_CREATE_SIGNATURE, IMAGE_TYPE_SIGNATURE
)
from app.utils.functions import now


class CtrSignature(BaseController):
    async def ctr_save_signature(self, cif_id: str, signatures: SignaturesRequest):
        # check len signature request
        if len(signatures.signatures) != 2:
            return self.response_exception(
                msg='signature must be equal 2',
                loc='ERROR_SAVE_SIGNATURE',
                detail='Can not save signature'
            )
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))
        identity = self.call_repos(await repos_get_last_identity(cif_id=cif_id, session=self.oracle_session))

        list_data_insert = [{
            'identity_id': identity.id,
            'image_type_id': IMAGE_TYPE_SIGNATURE,
            'image_url': signature.image_url,
            'hand_side_id': None,
            'finger_type_id': None,
            'vector_data': None,
            'active_flag': ACTIVE_FLAG_CREATE_SIGNATURE,
            'maker_id': self.current_user.user_id,
            'maker_at': now(),
            'identity_image_front_flag': None
        } for signature in signatures.signatures]

        data = self.call_repos(
            await repos_save_signature(
                cif_id=cif_id,
                list_data_insert=list_data_insert,
                session=self.oracle_session,
                created_by=self.current_user.full_name_vn
            )
        )

        return self.response(data=data)

    async def ctr_get_signature(self, cif_id: str):
        signature_data = self.call_repos(await repos_get_signature_data(cif_id=cif_id, session=self.oracle_session))

        return self.response(data=signature_data)
