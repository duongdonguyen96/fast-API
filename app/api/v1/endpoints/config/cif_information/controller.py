from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.cif_information.repository import (
    repos_get_customer_classification, repos_get_customer_economic_profession,
    repos_get_kyc_level
)


class CtrCifInfo(BaseController):
    async def ctr_customer_classification_info(self):
        customer_classification_info = self.call_repos(await repos_get_customer_classification(self.oracle_session))
        return self.response(customer_classification_info)

    async def ctr_customer_economic_profession_info(self):
        customer_economic_profession_info = self.call_repos(
            await repos_get_customer_economic_profession(self.oracle_session)
        )
        return self.response(customer_economic_profession_info)

    async def ctr_kyc_level_info(self):
        kyc_level_info = self.call_repos(
            await repos_get_kyc_level(self.oracle_session)
        )
        return self.response(kyc_level_info)
