from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.customer_relationship.repository import (
    repos_detail_customer_relationship, repos_save_customer_relationship
)


class CtrCustomerRelationship(BaseController):
    async def detail(self, cif_id: str):
        detail_customer_relationship_info = self.call_repos(await repos_detail_customer_relationship(cif_id=cif_id))
        return self.response(data=detail_customer_relationship_info)

    async def save(self, cif_id, customer_relationship_save_request):
        save_customer_relationship_info = self.call_repos(await repos_save_customer_relationship(
            cif_id=cif_id,
            created_by=self.current_user.full_name_vn
        ))
        return self.response(data=save_customer_relationship_info)
