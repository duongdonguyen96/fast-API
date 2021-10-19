from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownResponse


class ContactMethod(BaseSchema):
    email_flag: bool = Field(..., description='Email. `True`: có thể liên hệ. `False`: chưa thể liên hệ ')
    mobile_number_flag: bool = Field(..., description='Di động. `True`: có thể liên hệ. `False`: chưa thể liên hệ')


class PersonalResponse(BaseSchema):
    customer_id: int = Field(..., description='`ID` khách hàng')
    full_name_vn: str = Field(..., description='Tên tiếng việt khách hàng')
    gender: DropdownResponse = Field(..., description='Giới tính khách hàng')
    honorific: DropdownResponse = Field(..., description='Danh xưng khách hàng')
    date_of_birth: str = Field(..., description='Ngày sinh khách hàng')
    under_15_year_old_flag: bool = Field(..., description='Trạng thái dưới 15 tuổi')
    place_of_birth: DropdownResponse = Field(..., description='Nơi sinh khách hàng')
    country_of_birth: DropdownResponse = Field(..., description='Quốc gia sinh khách hàng')
    nationality: DropdownResponse = Field(..., description='Quốc tịch khách hàng')
    tax_number: str = Field(..., description='Mã số thuế cá nhân của khách hàng')
    resident_status: DropdownResponse = Field(..., description='Tình trạng cư trú khách hàng')
    mobile_number: str = Field(..., description='Điện thoại di động khách hàng')
    telephone_number: str = Field(..., description='Điện thoại bàn khách hàng')
    email: str = Field(..., description='Email khách hàng')
    contact_method: ContactMethod = Field(..., description='Hình thức liên hệ khách hàng')
    marital_status: DropdownResponse = Field(..., description='Tình trạng hôn nhân khách hàng')


class PersonalSuccessResponse(BaseSchema):
    basic_information: PersonalResponse = Field(..., description='Thông tin cơ bản khách hàng')
