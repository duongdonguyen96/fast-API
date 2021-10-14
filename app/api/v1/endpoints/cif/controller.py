from app.api.base.base import Controller
from app.api.v1.endpoints.cif.repository import repos_get_cif_info


class CtrCustomer(Controller):
    async def ctr_cif_info(self, customer_id: str):
        is_found, customer_cif_info = await repos_get_cif_info(customer_id)
        if not is_found:
            return self.response_exception(msg=customer_cif_info, loc="customer id")
        return self.response(customer_cif_info)
