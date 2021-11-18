from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.cif.other_information.schema import (
    OtherInformationUpdateRequest
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.other_information.model import (
    CustomerEmployee
)
from app.third_parties.oracle.models.master_data.others import (
    HrmEmployee, StaffType
)
from app.utils.constant.cif import BUSINESS_STAFF_TYPE_CODE, CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import now


async def repos_other_info(cif_id: str, session: Session) -> ReposReturn:
    customer_employee_engine = session.execute(
        select(
            Customer, StaffType, HrmEmployee
        ).join(
            CustomerEmployee, Customer.id == CustomerEmployee.customer_id
        ).join(
            StaffType, CustomerEmployee.staff_type_id == StaffType.id
        ).join(
            HrmEmployee, CustomerEmployee.employee_id == HrmEmployee.id
        ).filter(Customer.id == cif_id)
    )
    customer_employee = customer_employee_engine.all()

    if not customer_employee:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    sale_staff = None
    indirect_sale_staff = None

    # vị trí của customer trong query ở vị trí 0
    legal_agreement_flag = customer_employee[0][0].legal_agreement_flag
    advertising_marketing_flag = customer_employee[0][0].advertising_marketing_flag

    for _, staff_type, employee in customer_employee:
        if staff_type.code == BUSINESS_STAFF_TYPE_CODE:
            sale_staff = {
                "id": employee.id,
                "fullname_vn": employee.fullname_vn
            }
        else:
            indirect_sale_staff = {
                "id": employee.id,
                "fullname_vn": employee.fullname_vn
            }

    return ReposReturn(data={
        "legal_agreement_flag": legal_agreement_flag,
        "advertising_marketing_flag": advertising_marketing_flag,
        "sale_staff": sale_staff,
        "indirect_sale_staff": indirect_sale_staff,
    })




async def repos_update_other_info(cif_id: str, update_other_info_req: OtherInformationUpdateRequest) -> ReposReturn: # noqa
    if cif_id == CIF_ID_TEST:
        return ReposReturn(data={
            'created_at': now(),
            'created_by': 'system',
            'updated_at': now(),
            'updated_by': 'system'
        })
    else:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")
