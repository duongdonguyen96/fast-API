from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.passport.repository import (
    repos_get_passport_code, repos_get_passport_type
)


class CtrConfigPassport(BaseController):
    async def ctr_passport_type_info(self):
        passport_type_info = self.call_repos(await repos_get_passport_type(self.oracle_session))
        return self.response(passport_type_info)

    async def ctr_passport_code_info(self):
        passport_code_info = self.call_repos(await repos_get_passport_code(self.oracle_session))
        return self.response(passport_code_info)
