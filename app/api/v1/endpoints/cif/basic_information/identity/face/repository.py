from app.api.base.repository import ReposReturn
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST


async def repos_get_list_face(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=[
        {
            "date": "15/12/2021",
            "faces": [
                {
                    "identity_image_id": "1",
                    "image_url": "https://example.com/abc.png",
                    "created_at": "15/12/2021 06:07:08",
                    "similar_percent": 94
                },
                {
                    "identity_image_id": "2",
                    "image_url": "https://example.com/abc.png",
                    "created_at": "15/12/2021 06:07:08",
                    "similar_percent": 94
                }
            ]
        },
        {
            "date": "15/12/2021",
            "faces": [
                {
                    "identity_image_id": "3",
                    "image_url": "https://example.com/abc.png",
                    "created_at": "15/12/2021 06:07:08",
                    "similar_percent": 94
                },
                {
                    "identity_image_id": "4",
                    "image_url": "https://example.com/abc.png",
                    "created_at": "15/12/2021 06:07:08",
                    "similar_percent": 94
                }
            ]
        }
    ])
