from typing import Dict, Union

from app.utils.status.message import ERROR_CUSTOMER_ID_NOT_EXIST

CUSTOMER_CLASSIFICATION = {
    "id": "fd01b796-5ad1-4161-8e2c-2abe41390deb",
    "code": "CN",
    "name": "Cá nhân"
}
CUST_ECONOMIC_PROFESSTION = {
    "id": "b860d25e-0db2-496b-8bb7-76d6838d191a",
    "code": "KT1",
    "name": "Mã ngành KT"
}
KYC_LEVEL = {
    "id": "24152d4a-13c8-4720-a92d-2f2e784af6af",
    "code": "LV1",
    "name": "Level 1"
}
CUST_ID = "123"


async def repos_get_cif_info(customer_id: str) -> (bool, Union[str, Dict]):
    if customer_id == CUST_ID:
        return True, {
            "self_selected_cif_flag": True,
            "cif_number": "1234566",
            "customer_classification": CUSTOMER_CLASSIFICATION,
            "customer_economic_profession": CUST_ECONOMIC_PROFESSTION,
            "kyc_level": KYC_LEVEL,

        }
    else:
        return False, ERROR_CUSTOMER_ID_NOT_EXIST
