from app.api.base.repository import ReposReturn
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.status.message import ERROR_CIF_ID_NOT_EXIST


async def repos_get_data_finger(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "fingerprint_1": [
            {
                "image_url": "https://example.com/abc.png",
                "hand_side": {
                    "id": "1",
                    "code": "taytrai",
                    "name": "bàn tay trái"
                },
                "finger_type": {
                    "id": "1",
                    "code": "ngontro",
                    "name": "ngón trỏ"
                }
            },
            {
                "image_url": "https://example.com/abc.png",
                "hand_side": {
                    "id": "1",
                    "code": "taytrai",
                    "name": "bàn tay trái"
                },
                "finger_type": {
                    "id": "2",
                    "code": "ngongiua",
                    "name": "ngón giữa"
                }
            },
            {
                "image_url": "https://example.com/abc.png",
                "hand_side": {
                    "id": "1",
                    "code": "taytrai",
                    "name": "bàn tay trái"
                },
                "finger_type": {
                    "id": "3",
                    "code": "ngoncai",
                    "name": "ngón cái"
                }
            }
        ],
        "fingerprint_2": [
            {
                "image_url": "https://example.com/abc.png",
                "hand_side": {
                    "id": "2",
                    "code": "tayphai",
                    "name": "bàn tay phải"
                },
                "finger_type": {
                    "id": "1",
                    "code": "ngontro",
                    "name": "ngón trỏ"
                }
            },
            {
                "image_url": "https://example.com/abc.png",
                "hand_side": {
                    "id": "2",
                    "code": "tayphai",
                    "name": "bàn tay phải"
                },
                "finger_type": {
                    "id": "2",
                    "code": "ngongiua",
                    "name": "ngón giữa"
                }
            },
            {
                "image_url": "https://example.com/abc.png",
                "hand_side": {
                    "id": "2",
                    "code": "tayphai",
                    "name": "bàn tay phẩi"
                },
                "finger_type": {
                    "id": "3",
                    "code": "ngoncai",
                    "name": "ngón cái"
                }
            }
        ]
    })
