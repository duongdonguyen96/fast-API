from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.repository import (
    check_cif_number, repos_get_data_finger, repos_save_fingerprint
)
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.schema import (
    TwoFingerPrintRequest
)
from app.api.v1.endpoints.cif.repository import (
    repos_get_image_type, repos_get_last_identity
)
from app.utils.constant.cif import (
    ACTIVE_FLAG_CREATE_FINGERPRINT, FRONT_FLAG_CREATE_FINGERPRINT,
    IMAGE_TYPE_FINGERPRINT
)
from app.utils.functions import now


class CtrFingerPrint(BaseController):
    async def ctr_save_fingerprint(self, cif_id: str, finger_request: TwoFingerPrintRequest):
        flag_customer = self.call_repos(await check_cif_number(cif_id, self.oracle_session)) # noqa

        image_type = self.call_repos(await repos_get_image_type(self.oracle_session, IMAGE_TYPE_FINGERPRINT))
        identity = self.call_repos(await repos_get_last_identity(cif_id, self.oracle_session))

        list_data = []
        list_data.extend(finger_request.fingerprint_1)
        list_data.extend(finger_request.fingerprint_2)

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
        } for item in list_data]

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
