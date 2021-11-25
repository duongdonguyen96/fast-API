from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.personal.repository import (
    repos_get_ethnic, repos_get_gender, repos_get_honorific,
    repos_get_nationality, repos_get_religion
)


class CtrConfigPersonal(BaseController):
    async def ctr_gender_info(self):
        gender_info = self.call_repos(await repos_get_gender(self.oracle_session))
        return self.response(gender_info)

    async def ctr_nationality_info(self):
        nationality_info = self.call_repos(await repos_get_nationality(self.oracle_session))
        return self.response(nationality_info)

    async def ctr_ethnic_info(self):
        ethnic_info = self.call_repos(await repos_get_ethnic(self.oracle_session))
        return self.response(ethnic_info)

    async def ctr_religion_info(self):
        religion_info = self.call_repos(await repos_get_religion(self.oracle_session))
        return self.response(religion_info)

    async def ctr_honorific_info(self):
        honorific_info = self.call_repos(await repos_get_honorific(self.oracle_session))
        return self.response(honorific_info)
