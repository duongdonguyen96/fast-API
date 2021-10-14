from typing import Any, Dict, Union

from app.utils.status.message import (
    ERROR_INVALID_TOKEN, USER_ID_NOT_EXIST, USERNAME_OR_PASSWORD_INVALID
)

USER_ID = "9651cdfd9a9a4eb691f9a3a125ac46b0"
USER_TOKEN = "OTY1MWNkZmQ5YTlhNGViNjkxZjlhM2ExMjVhYzQ2YjA6N2VlN2E2ZTg1MTUzN2M2YzFmYWIwMWQzODYzMWU4YTIx"

USER_INFO = {
    "user_id": str(USER_ID),
    "user_name": "dev1",
    "full_name": "Developer 1",
    "avatar_url": "cdn/users/avatar/dev1.jpg"
}


async def repos_login(username: str, password: str) -> (bool, Union[str, Any]):
    if username == 'dev1' and password == '12345678':
        return True, {
            "token": USER_TOKEN,
            "user_info": USER_INFO
        }
    else:
        return False, USERNAME_OR_PASSWORD_INVALID


async def repos_check_token(token: str) -> (bool, Union[str, Any]):
    if token == USER_TOKEN:
        return True, USER_INFO
    else:
        return False, ERROR_INVALID_TOKEN


async def repos_get_user_info(user_id: str) -> (bool, Union[str, Dict]):
    if user_id == USER_ID:
        return True, USER_INFO
    else:
        return False, USER_ID_NOT_EXIST
