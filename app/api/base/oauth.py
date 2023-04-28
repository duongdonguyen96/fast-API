from fastapi import Depends
from fastapi import FastAPI, HTTPException
import jwt
from datetime import date, datetime, timedelta
from typing import Union, Dict

from app.api.base.schema import UserInfo
from app.utils import error_messages as message
from app.utils.constant import constant as c
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

app = FastAPI()

oauth = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth)):
    _status, data = await decode_jwt(
        token=credentials.credentials,
        secret_key=c.SECRET_KEY,
        algorithms=c.ALGORITHM
    )
    if not _status:
        raise HTTPException(status_code=404, detail=data)
    try:
        data.pop("exp")
        data = UserInfo(**data)
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    return data


async def encode_jwt(data, minutes, secret_key, algorithm) -> (bool, Union[str, Dict]):
    try:
        to_encode = data.copy()
        to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=minutes)})
        token = jwt.encode(to_encode, secret_key, algorithm=algorithm)

    except Exception as ex:
        return False, str(ex)

    return True, token


async def decode_jwt(token: str, secret_key, algorithms) -> (bool, Union[str, Dict]):
    try:
        data = jwt.decode(token, secret_key, algorithms=algorithms)

    except jwt.ExpiredSignatureError:
        return False, message.TOKEN_EXPIRED
    except jwt.exceptions.InvalidSignatureError:
        return False, message.ERROR_INVALID_TOKEN
    except Exception as ex:
        return False, str(ex)

    return True, data
