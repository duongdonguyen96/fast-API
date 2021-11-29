from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.customer import (
    CustomerClassification, CustomerEconomicProfession
)
from app.third_parties.oracle.models.master_data.others import KYCLevel


class CtrCifInfo(BaseController):
    async def ctr_customer_classification_info(self):
        customer_classification_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=CustomerClassification,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(customer_classification_info)

    async def ctr_customer_economic_profession_info(self):
        customer_economic_profession_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=CustomerEconomicProfession,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(customer_economic_profession_info)

    async def ctr_kyc_level_info(self):
        kyc_level_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=KYCLevel,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(kyc_level_info)
