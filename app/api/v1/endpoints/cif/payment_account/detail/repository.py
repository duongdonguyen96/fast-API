from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.cif.payment_account.detail.schema import (
    SavePaymentAccountRequest
)
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import now

REQUIREMENT_PAYMENT_ACCOUNT_INFO_DETAIL = {
    "self_selected_account_flag": True,
    "currency": {
        "id": "1",
        "code": "VND",
        "name": "Việt Nam Đồng"
    },
    "account_type": {
        "id": "1",
        "code": "LOCPHAT",
        "name": "Lộc Phát"
    },
    "account_class": {
        "id": "1",
        "code": "LOAIHINH1",
        "name": "Loại Hình 1"
    },
    "account_structure_type_level_1": {
        "id": "1",
        "code": "LEVEL1",
        "name": "11 số"
    },
    "account_structure_type_level_2": {
        "id": "2",
        "code": "LEVEL2",
        "name": "Lộc Phát"
    },
    "account_structure_type_level_3": {
        "id": "3",
        "code": "LEVEL3",
        "name": "6868"
    },
    "casa_account": {
        "id": "1",
        "account_number": "XXXXXXXX6868"
    },
    "account_salary_organization_account": "13245678912",
    "account_salary_organization_name": "Công ty ABC"
}

NO_REQUIREMENT_PAYMENT_ACCOUNT_INFO_DETAIL = {
    "self_selected_account_flag": False,
    "currency": {
        "id": "1",
        "code": "VND",
        "name": "Việt Nam Đồng"
    },
    "account_type": {
        "id": "1",
        "code": "LOCPHAT",
        "name": "Lộc Phát"
    },
    "account_class": {
        "id": "1",
        "code": "LOAIHINH1",
        "name": "Loại Hình 1"
    },
    "account_structure_type_level_1": {
        "id": None,
        "code": None,
        "name": None
    },
    "account_structure_type_level_2": {
        "id": None,
        "code": None,
        "name": None
    },
    "account_structure_type_level_3": {
        "id": None,
        "code": None,
        "name": None
    },
    "casa_account": {
        "id": None,
        "account_number": None
    },
    "account_salary_organization_account": "13245678912",
    "account_salary_organization_name": None
}


async def repos_detail_payment_account(cif_id: str):
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    return ReposReturn(data=REQUIREMENT_PAYMENT_ACCOUNT_INFO_DETAIL)


async def repos_save_payment_account(
        cif_id: str,
        payment_account_save_request: SavePaymentAccountRequest,
        created_by
):
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })
