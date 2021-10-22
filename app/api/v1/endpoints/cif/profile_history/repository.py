from app.api.base.repository import ReposReturn
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST


async def repos_profile_history(cif_id: str) -> ReposReturn:
    if cif_id == CIF_ID_TEST:
        return ReposReturn(data=[
            {

                "date": "string",
                "logs":

                    [

                        {
                            "user_id": "string",
                            "full_name": "string",
                            "user_avatar_url": "string",
                            "id": "string",
                            "created_at": "2019-08-24T14:15:22Z",
                            "content": "string"
                        },
                        {
                            "user_id": "string",
                            "full_name": "string",
                            "user_avatar_url": "string",
                            "id": "string",
                            "created_at": "2019-08-24T14:15:22Z",
                            "content": "string"
                        }
                    ]

            },
            {

                "date": "string",
                "logs":

                    [

                        {
                            "user_id": "string",
                            "full_name": "string",
                            "user_avatar_url": "string",
                            "id": "string",
                            "created_at": "2019-08-24T14:15:22Z",
                            "content": "string"
                        },
                        {
                            "user_id": "string",
                            "full_name": "string",
                            "user_avatar_url": "string",
                            "id": "string",
                            "created_at": "2019-08-24T14:15:22Z",
                            "content": "string"
                        }
                    ]
            }
        ]
        )
    else:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')
