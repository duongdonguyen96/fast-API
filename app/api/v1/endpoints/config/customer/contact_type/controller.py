from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.customer.contact_type.repository import (
    repos_get_customer_contact_type
)


class CtrConfigContactType(BaseController):
    async def ctr_customer_contact_type_info(self):
        customer_contact_type_infos = self.call_repos(
            await repos_get_customer_contact_type(session=self.oracle_session))

        return self.response(customer_contact_type_infos)
