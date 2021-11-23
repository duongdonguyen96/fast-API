from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.repository import (
    repos_get_crm_finger_type, repos_get_crm_hand_side, repos_get_data_finger,
    repos_save_fingerprint
)
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.schema import (
    TwoFingerPrintRequest
)
from app.api.v1.endpoints.cif.repository import (
    repos_get_image_type, repos_get_initializing_customer,
    repos_get_last_identity
)
from app.utils.constant.cif import (
    ACTIVE_FLAG_CREATE_FINGERPRINT, FRONT_FLAG_CREATE_FINGERPRINT,
    IMAGE_TYPE_FINGERPRINT
)
from app.utils.functions import now


class CtrFingerPrint(BaseController):
    async def ctr_save_fingerprint(self, cif_id: str, finger_request: TwoFingerPrintRequest):
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        image_type = self.call_repos(await repos_get_image_type(IMAGE_TYPE_FINGERPRINT, session=self.oracle_session))
        identity = self.call_repos(await repos_get_last_identity(cif_id, self.oracle_session))

        fingerprints = []
        fingerprints.extend(finger_request.fingerprint_1)
        fingerprints.extend(finger_request.fingerprint_2)

        list_data_inserts = [{
            'identity_id': identity.id,
            'image_type_id': image_type.code,
            'image_url': item.image_url,
            'hand_side_id': item.hand_side.id,
            'finger_type_id': item.finger_type.id,
            'vector_data': None,
            'active_flag': ACTIVE_FLAG_CREATE_FINGERPRINT,
            'maker_id': self.current_user.user_id,
            'maker_at': now(),
            'identity_image_front_flag': FRONT_FLAG_CREATE_FINGERPRINT
        } for item in fingerprints]

        hand_side_ids = []
        finger_type_ids = []

        for item in list_data_inserts:
            hand_side_ids.append(item['hand_side_id'])
            finger_type_ids.append(item['finger_type_id'])

        hand_side_ids = list(set(hand_side_ids))
        finger_type_ids = list(set(finger_type_ids))

        # check exits hand_side_ids, finger_type_ids
        self.call_repos(await repos_get_crm_hand_side(hand_side_ids=hand_side_ids, session=self.oracle_session))
        self.call_repos(await repos_get_crm_finger_type(finger_type_ids=finger_type_ids, session=self.oracle_session))

        data = self.call_repos(
            await repos_save_fingerprint(
                cif_id=cif_id,
                session=self.oracle_session,
                list_data_inserts=list_data_inserts,
                created_by=self.current_user.full_name_vn
            )
        )
        return self.response(data=data)

    async def ctr_get_fingerprint(self, cif_id: str):
        fingerprint_data = self.call_repos(await repos_get_data_finger(cif_id, self.oracle_session))
        return self.response(data=fingerprint_data)
