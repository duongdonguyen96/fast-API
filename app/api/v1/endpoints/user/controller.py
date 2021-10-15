from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.repository import (
    repos_get_list_user, repos_get_user_info, repos_login
)
from app.api.v1.endpoints.user.schema import AuthReq


class CtrUser(BaseController):
    async def ctr_get_list_user(self):
        users = self.call_repos(await repos_get_list_user())
        return self.response_paging(data=users, current_page=1, total_page=1, total_item=len(users))

    async def ctr_login(self, login_req: AuthReq):
        auth_res = self.call_repos(await repos_login(username=login_req.username, password=login_req.password))

        return self.response(data=auth_res)

    async def ctr_get_current_user_info(self):
        return self.response(data=self.current_user)

    async def ctr_get_user_info(self, user_id: str):
        info_user_data = self.call_repos(await repos_get_user_info(user_id))

        return self.response(data=info_user_data)
