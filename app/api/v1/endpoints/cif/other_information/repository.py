from sqlalchemy import select, update
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
from app.utils.constant.cif import (
    STAFF_TYPE_BUSINESS_CODE, STAFF_TYPE_REFER_INDIRECT_CODE
)
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

    for _, staff_type, employee in customer_employee:
        if staff_type.code == STAFF_TYPE_BUSINESS_CODE:
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
        # lấy ra data ở vị trí 0 trong query sau đó lấy ra customer ở vị trí 0
        "legal_agreement_flag": customer_employee[0][0].legal_agreement_flag,
        "advertising_marketing_flag": customer_employee[0][0].advertising_marketing_flag,
        "sale_staff": sale_staff,
        "indirect_sale_staff": indirect_sale_staff,
    })


async def repos_update_other_info(cif_id: str, update_other_info_req: OtherInformationUpdateRequest,
                                  session: Session) -> ReposReturn:

    session.execute(
        update(Customer).filter(Customer.id == cif_id).values(
            legal_agreement_flag=update_other_info_req.legal_agreement_flag,
            advertising_marketing_flag=update_other_info_req.advertising_marketing_flag
        )
    )

    new_customer_employees = []
    if update_other_info_req.sale_staff:
        new_customer_employees.append(
            {
                "staff_type_id": STAFF_TYPE_BUSINESS_CODE,
                "employee_id": update_other_info_req.sale_staff.id,
                "customer_id": cif_id
            }
        )

    if update_other_info_req.indirect_sale_staff:
        new_customer_employees.append(
            {
                "staff_type_id": STAFF_TYPE_REFER_INDIRECT_CODE,
                "employee_id": update_other_info_req.indirect_sale_staff.id,
                "customer_id": cif_id
            }
        )

    data_insert = [CustomerEmployee(**data_insert) for data_insert in new_customer_employees]
    session.bulk_save_objects(data_insert)

    session.commit()

    return ReposReturn(data={
        'created_at': now(),
        'created_by': 'system',
        'updated_at': now(),
        'updated_by': 'system'
    })
