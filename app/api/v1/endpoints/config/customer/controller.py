from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.customer.repository import (
    repos_get_customer_contact_type, repos_get_customer_type
)


class CtrConfigCustomer(BaseController):
    async def ctr_customer_type_info(self):
        customer_type_info = self.call_repos(await repos_get_customer_type(self.oracle_session))
        return self.response(customer_type_info)

    async def ctr_customer_contact_type_info(self):
        customer_contact_type_info = self.call_repos(await repos_get_customer_contact_type(self.oracle_session))
        return self.response(customer_contact_type_info)
