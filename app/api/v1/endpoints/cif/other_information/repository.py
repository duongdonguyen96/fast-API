from app.api.base.repository import ReposReturn
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.status.message import ERROR_CIF_ID_NOT_EXIST


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
