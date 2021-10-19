from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.cif.other_information.schema import (
    OtherInformationUpdateRequest
)
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import now


async def repos_other_info(cif_id: str) -> ReposReturn:
    if cif_id == CIF_ID_TEST:
        return ReposReturn(data={
            "legal_agreement_flag": True,
            "advertising_marketing_flag": True,
            "sale_staff": {
                "id": "02781",
                "code": "02781",
                "name": "Nguyễn Thanh Tuyền"
            },
            "indirect_sale_staff": {
                "id": "02781",
                "code": "02781",
                "name": "Nguyễn Thanh Tuyền"
            }
        })
    else:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")


async def repos_update_other_info(cif_id: str, update_other_info_req: OtherInformationUpdateRequest) -> ReposReturn: # noqa
    if cif_id == CIF_ID_TEST:
        return ReposReturn(data={
            'created_at': now(),
            'created_by': 'system',
            'updated_at': now(),
            'updated_by': 'system'
        })
    else:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")
