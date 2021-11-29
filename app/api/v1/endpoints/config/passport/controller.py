from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.identity import (
    PassportCode, PassportType
)


class CtrConfigPassport(BaseController):
    async def ctr_passport_type_info(self):
        passport_type_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=PassportType,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(passport_type_info)

    async def ctr_passport_code_info(self):
        passport_code_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=PassportCode,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(passport_code_info)
