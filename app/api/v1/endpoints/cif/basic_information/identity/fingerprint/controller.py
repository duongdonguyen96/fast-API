from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.repository import (
    repos_get_data_finger, repos_save_fingerprint
)
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.schema import (
    TwoFingerPrintRequest
)
from app.api.v1.endpoints.cif.repository import (
    repos_get_customer_identity, repos_get_initializing_customer
)
from app.third_parties.oracle.models.master_data.identity import (
    FingerType, HandSide
)
from app.utils.constant.cif import (
    ACTIVE_FLAG_CREATE_FINGERPRINT, FRONT_FLAG_CREATE_FINGERPRINT,
    IMAGE_TYPE_FINGERPRINT
)
from app.utils.functions import now


class CtrFingerPrint(BaseController):
    async def ctr_save_fingerprint(self, cif_id: str, finger_request: TwoFingerPrintRequest):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        fingerprints = []
        fingerprints.extend(finger_request.fingerprint_1)
        fingerprints.extend(finger_request.fingerprint_2)

        hand_side_ids = []
        finger_type_ids = []

        for item in fingerprints:
            hand_side_ids.append(item.hand_side.id)
            finger_type_ids.append(item.finger_type.id)

        # check exits hand_side_ids, finger_type_ids
        await self.get_model_objects_by_ids(model_ids=hand_side_ids, model=HandSide, loc='hand_side -> id')
        await self.get_model_objects_by_ids(model_ids=finger_type_ids, model=FingerType, loc='finger_type -> id')

        identity = self.call_repos(await repos_get_customer_identity(cif_id, self.oracle_session))

        list_data_insert = [{
            'identity_id': identity.id,
            'image_type_id': IMAGE_TYPE_FINGERPRINT,
            'image_url': item.image_url,
            'hand_side_id': item.hand_side.id,
            'finger_type_id': item.finger_type.id,
            'vector_data': None,
            'active_flag': ACTIVE_FLAG_CREATE_FINGERPRINT,
            'maker_id': self.current_user.user_id,
            'maker_at': now(),
            'identity_image_front_flag': FRONT_FLAG_CREATE_FINGERPRINT
        } for item in fingerprints]

        data = self.call_repos(
            await repos_save_fingerprint(
                cif_id=cif_id,
                session=self.oracle_session,
                list_data_insert=list_data_insert,
                created_by=self.current_user.full_name_vn
            )
        )
        return self.response(data=data)

    async def ctr_get_fingerprint(self, cif_id: str):
        fingerprint_data = self.call_repos(await repos_get_data_finger(cif_id, self.oracle_session))
        return self.response(data=fingerprint_data)
