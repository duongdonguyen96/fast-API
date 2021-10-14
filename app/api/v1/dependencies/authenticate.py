from typing import Callable, Optional, Union

from fastapi import Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.api.v1.endpoints.user.repository import repos_check_token
from app.api.v1.endpoints.user.schema import UserInfoRes
from app.utils.status.except_custom import ExceptionHandle
from app.utils.status.message import ERROR_INVALID_TOKEN


def get_current_user_from_header(is_require_login: bool = True) -> Callable:
    return _get_authorization_header if is_require_login else _get_authorization_header_optional


async def _get_authorization_header(
        scheme_and_credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())
) -> UserInfoRes:
    is_valid, user_info = await repos_check_token(token=scheme_and_credentials.credentials)
    if is_valid:
        return UserInfoRes(**user_info)
    else:
        raise ExceptionHandle(
            errors=[{'loc': None, 'msg': ERROR_INVALID_TOKEN}],
            status_code=status.HTTP_400_BAD_REQUEST
        )


async def _get_authorization_header_optional(
        scheme_and_credentials: Optional[HTTPAuthorizationCredentials] = Security(HTTPBearer(auto_error=False))
) -> Union[UserInfoRes, None]:
    if scheme_and_credentials:
        return await _get_authorization_header(
            scheme_and_credentials=scheme_and_credentials
        )
    return None
