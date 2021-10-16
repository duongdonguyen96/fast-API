from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.repository import repos_get_cif_info


class CtrCustomer(BaseController):
    async def ctr_cif_info(self, customer_id: str):
        is_found, cif_info = await repos_get_cif_info(customer_id)
        if not is_found:
            return self.response_exception(msg=cif_info, loc="customer id")
        return self.response(cif_info)
