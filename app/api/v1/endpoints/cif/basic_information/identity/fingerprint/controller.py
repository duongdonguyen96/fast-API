from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.repository import (
    check_cif_number, repos_get_data_finger, repos_get_identity_id,
    repos_save_fingerprint
)
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.schema import (
    TwoFingerPrintRequest
)
from app.utils.constant.cif import (
    ACTIVE_FLAG_CREATE_FINGERPRINT, FRONT_FLAG_CREATE_FINGERPRINT
)
from app.utils.functions import now


class CtrFingerPrint(BaseController):
    async def ctr_save_fingerprint(self, cif_id: str, finger_request: TwoFingerPrintRequest):
        # TODO: xây dựng hàm kiểm tra điều kiện trước khi tạo vân tay
        query_data = self.call_repos(await check_cif_number(cif_id, self.oracle_session)) # noqa

        identity = self.call_repos(await repos_get_identity_id(cif_id, self.oracle_session))

        list_data_insert = []
        for item in finger_request.fingerprint_2:
            list_data_insert.append(
                {
                    'identity_id': identity.id,
                    'identity_type_id': identity.identity_type_id,
                    'image_url': item.image_url,
                    'hand_side_id': item.hand_side.id,
                    'finger_type_id': item.finger_type.id,
                    'vector_data': None,
                    'active_flag': ACTIVE_FLAG_CREATE_FINGERPRINT,
                    'maker_id': self.current_user.user_id,
                    'maker_at': now(),
                    'identity_image_front_flag': FRONT_FLAG_CREATE_FINGERPRINT
                }
            )
        for item in finger_request.fingerprint_1:
            list_data_insert.append(
                {
                    'identity_id': identity.id,
                    'identity_type_id': identity.identity_type_id,
                    'image_url': item.image_url,
                    'hand_side_id': item.hand_side.id,
                    'finger_type_id': item.finger_type.id,
                    'vector_data': None,
                    'active_flag': ACTIVE_FLAG_CREATE_FINGERPRINT,
                    'maker_id': self.current_user.user_id,
                    'maker_at': now(),
                    'identity_image_front_flag': FRONT_FLAG_CREATE_FINGERPRINT
                }
            )

        data = self.call_repos(
            await repos_save_fingerprint(
                cif_id=cif_id,
                oracle_session=self.oracle_session,
                list_data_insert=list_data_insert,
                created_by=self.current_user.full_name_vn
            )
        )
        return self.response(data=data)

    async def ctr_get_fingerprint(self, cif_id: str):
        fingerprint_data = self.call_repos(await repos_get_data_finger(cif_id, self.oracle_session))
        return self.response(data=fingerprint_data)
