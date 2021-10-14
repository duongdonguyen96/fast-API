from app.api.base.base import Controller
from app.api.v1.endpoints.user.repository import (
    repos_get_user_info, repos_login
)
from app.api.v1.endpoints.user.schema import AuthReq


class CtrUser(Controller):
    async def ctr_login(self, login_req: AuthReq):
        is_auth, auth_res = await repos_login(username=login_req.username, password=login_req.password)
        if not is_auth:
            return self.response_exception(msg=auth_res, loc="username, password")

        return self.response(data=auth_res)

    async def ctr_get_current_user_info(self):
        return self.response(data=self.current_user)

    async def ctr_get_user_info(self, user_id: str):
        is_found, info_user_data = await repos_get_user_info(user_id)
        if not is_found:
            return self.response_exception(msg=info_user_data, loc="user_id")

        return self.response(data=info_user_data)
