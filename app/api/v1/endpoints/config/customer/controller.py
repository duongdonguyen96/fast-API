from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.customer import (
    CustomerContactType, CustomerType
)


class CtrConfigCustomer(BaseController):
    async def ctr_customer_type_info(self):
        customer_type_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=CustomerType,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(customer_type_info)

    async def ctr_customer_contact_type_info(self):
        customer_contact_type_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=CustomerContactType,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(customer_contact_type_info)
