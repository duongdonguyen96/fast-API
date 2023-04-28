from sqlalchemy import text

from app.api.base.controller import BaseController
from app.api.base.oauth import encode_jwt
from app.api.base.schema import Authentication
from app.api.v1.endpoints.train.customer.repository import _get_user_by_username, create_user, get_all_user
from app.api.v1.endpoints.train.customer.schema import CreateUserRq

from app.utils.constant import constant as c

from app.utils.functions import generate_uuid, now, hash_password, verify_password
from app.utils import error_messages as ms


class CtrUser(BaseController):

    async def ctr_login(self, user: Authentication):
        user_db = self.call_repos(await _get_user_by_username(session=self.oracle_session, username=user.username))
        if not user_db:
            return self.response_exception(
                msg=ms.USER_IS_NOT_EXIST,
                loc=self.ctr_login.__name__
            )

        if not verify_password(user.password, user_db.password):
            return self.response_exception(
                msg=ms.PASSWORD_INVALID,
                loc=self.ctr_login.__name__
            )

        user_info = {
            "user_id": user_db.id,
            "username": user_db.username,
            "full_name": user_db.full_name,
            "email": user_db.email,
            "department_id": user_db.department_id,
            "company_id": user_db.company_id
        }

        status, token = await encode_jwt(
            data=user_info,
            minutes=c.ACCESS_TOKEN_EXPIRE_1_DAY,
            secret_key=c.SECRET_KEY,
            algorithm=c.ALGORITHM
        )

        if not status:
            return self.response_exception(
                msg=ms.LOGIN_ERROR,
                detail=token,
                loc=self.ctr_login.__name__
            )

        data = {
            "access_token": token,
            "user_info": user_info,
        }

        return self.response(data=data)

    async def ctr_create_user(self, user: CreateUserRq):
        user_db = self.call_repos(await _get_user_by_username(session=self.oracle_session, username=user.username))
        if user_db:
            if user_db.username == user.username:
                return self.response_exception(
                    msg=ms.VALIDATE_ERROR,
                    detail="username đã tồn tại",
                    loc="ctr_create_user"
                )

        _user = {
            'id': generate_uuid(),
            'full_name': user.full_name,
            'email': user.email,
            'phone': user.phone,
            'gender': user.gender,
            'username': user.username,
            'password': hash_password(user.password)
        }

        data = self.call_repos(await create_user(user=_user, session=self.oracle_session))

        return self.response(data=data)

    async def get_all_user(self, params):
        query = self.call_repos(await get_all_user(session=self.oracle_session))

        data = self.response_paging(query=query, params=params)

        res = [
            {'id': user.id,
             'full_name': user.full_name,
             'email': user.email,
             'gender': user.gender,
             'is_active': user.is_active,
             'phone': user.phone,
             'username': user.username
             } for user in data['data']
        ]

        return {
            'data': res,
            'total_item': data['total_item'],
            'total_page': data['total_page'],
            'current_page': data['current_page']
        }

        # return self.response(data=all_users)

    async def change_password(self, user):
        user_db = self.call_repos(await _get_user_by_username(session=self.oracle_session, username=user.username))

        if not user_db:
            return self.response_exception(
                msg=ms.VALIDATE_ERROR,
                detail="username không tồn tại",
                loc=self.change_password.__name__
            )

        if not verify_password(user.old_password, user_db.password):
            return self.response_exception(
                msg=ms.VALIDATE_ERROR,
                detail="Mật khẩu sai",
                loc="change_password"
            )
        user_db.password = hash_password(user.new_password)

        self.oracle_session.commit()

        return self.response(data='Thay đổi mật khẩu thành công!!')

    async def get_chart_1(self):
        return {
            'month_1': 10,
            'month_2': 15,
            'month_3': 10,
            'month_4': 15,
            'month_5': 10,
            'month_6': 15,
            'month_7': 10,
            'month_8': 15,
            'month_9': 10,
            'month_10': 15,
            'month_11': 10,
            'month_12': 15
        }

    async def get_chart_2(self):
        return {
            'male': 100,
            'female': 80,
            'other': 2
        }
