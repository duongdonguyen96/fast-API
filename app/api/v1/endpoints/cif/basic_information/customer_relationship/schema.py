from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.schemas.cif import RelationshipResponse
from app.api.v1.schemas.utils import DropdownRequest


########################################################################################################################
# Response
########################################################################################################################
# Thông tin mối quan hệ khách hàng -> Danh sách mối quan hệ khách hàng
class CustomerRelationshipResponse(RelationshipResponse):
    id: str = Field(..., description="ID mối quan hệ khách hàng")
    avatar_url: Optional[str] = Field(..., description="URL avatar mối quan hệ khách hàng")


# Thông tin mối quan hệ khách hàng
class DetailCustomerRelationshipResponse(BaseSchema):
    customer_relationship_flag: bool = Field(..., description="Cờ có người mối quan hệ khách hàng không")
    number_of_customer_relationship: int = Field(..., description="Số mối quan hệ khách hàng")
    relationships: List[CustomerRelationshipResponse] = Field(..., description="Danh sách mối quan hệ khách hàng")


########################################################################################################################
# Request Body
########################################################################################################################
# Thông tin mối quan hệ khách hàng
class SaveCustomerRelationshipRequest(BaseSchema):
    cif_number: str = CustomField().CIFNumberField
    customer_relationship: DropdownRequest = Field(..., description="Mối quan hệ với khách hàng")
