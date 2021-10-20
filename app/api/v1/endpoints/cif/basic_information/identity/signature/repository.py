from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.cif.basic_information.identity.signature.schema import (
    SignaturesRequest
)
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import now


async def repos_save_signature(cif_id: str, signature: SignaturesRequest, created_by: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_get_signature_data(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "customer_signatures": [
            {
                "created_date": "2021-06-12",
                "identity_image_transaction_1": "http://example.com/abc.png",
                "identity_image_transaction_2": "http://example.com/abc.png",
                "checked_flag": True
            },
            {
                "created_date": "2021-05-30",
                "identity_image_transaction_1": "http://example.com/abc.png",
                "identity_image_transaction_2": "http://example.com/abc.png",
                "checked_flag": False
            }
        ],
        "compare_signature": {
            "compare_image_url": "http://example.com/abc.png",
            "similar_percent": 94
        }
    })
