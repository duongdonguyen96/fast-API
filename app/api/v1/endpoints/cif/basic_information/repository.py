from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.contact.model import (
    CustomerAddress
)
from app.third_parties.oracle.models.cif.basic_information.guardian_and_relationship.model import (
    CustomerPersonalRelationship
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.basic_information.personal.model import (
    CustomerIndividualInfo
)
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.customer import CustomerGender
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.utils.constant.cif import (
    CONTACT_ADDRESS_CODE, CUSTOMER_COMPLETED_FLAG
)
from app.utils.error_messages import ERROR_CIF_NUMBER_NOT_EXIST
from app.utils.functions import dropdown


async def repos_get_customer_detail(
        cif_number: str,
        session: Session
):
    rows = session.execute(
        select(
            Customer.id,
            Customer.avatar_url,
            Customer.cif_number,
            Customer.full_name_vn,
            Customer.telephone_number,
            Customer.mobile_number,
            Customer.email,
            CustomerIndividualInfo,
            CustomerGender,
            AddressCountry,
            CustomerIdentity,
            PlaceOfIssue,
            CustomerAddress,
            AddressProvince,
            AddressDistrict,
            AddressWard,
        )
        .join(CustomerIndividualInfo, Customer.id == CustomerIndividualInfo.customer_id)
        .join(CustomerGender, CustomerIndividualInfo.gender_id == CustomerGender.id)
        .join(AddressCountry, Customer.nationality_id == AddressCountry.id)
        .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
        .join(PlaceOfIssue, CustomerIdentity.place_of_issue_id == PlaceOfIssue.id)
        .join(CustomerAddress, Customer.id == CustomerAddress.customer_id)
        .join(AddressProvince, CustomerAddress.address_province_id == AddressProvince.id)
        .join(AddressDistrict, CustomerAddress.address_district_id == AddressDistrict.id)
        .join(AddressWard, CustomerAddress.address_ward_id == AddressWard.id)
        .filter(
            Customer.cif_number == cif_number,
            Customer.complete_flag == CUSTOMER_COMPLETED_FLAG
        )
    ).all()

    customer_info = rows[0]

    if not rows:
        return ReposReturn(
            is_error=True,
            msg=ERROR_CIF_NUMBER_NOT_EXIST,
            loc="cif_number"
        )

    # vì join với address bị lặp dữ liệu nên cần tạo dict địa chỉ dựa trên id để trả về
    customer_id__address_info = {
        "contact_address": None,
        "resident_address": None,
    }
    for row in rows:
        address = {
            "province": dropdown(row.AddressProvince),
            "district": dropdown(row.AddressDistrict),
            "ward": dropdown(row.AddressWard),
            "number_and_street": row.CustomerAddress.address
        }
        if row.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
            customer_id__address_info["contact_address"] = address
        else:
            customer_id__address_info["resident_address"] = address

    return ReposReturn(data={
        "id": customer_info.id,
        "avatar_url": customer_info.avatar_url,
        "basic_information": {
            "cif_number": customer_info.cif_number,
            "full_name_vn": customer_info.full_name_vn,
            "date_of_birth": customer_info.CustomerIndividualInfo.date_of_birth,
            "gender": dropdown(customer_info.CustomerGender),
            "nationality": dropdown(customer_info.AddressCountry),
            "telephone_number": customer_info.telephone_number,
            "mobile_number": customer_info.mobile_number,
            "email": customer_info.email,
        },
        "identity_document": {
            "identity_number": customer_info.CustomerIdentity.identity_num,
            "issued_date": customer_info.CustomerIdentity.issued_date,
            "place_of_issue": dropdown(customer_info.PlaceOfIssue),
            "expired_date": customer_info.CustomerIdentity.expired_date
        },
        "address_information": {
            "contact_address": customer_id__address_info["contact_address"],
            "resident_address": customer_id__address_info["resident_address"],
        }
    })


async def repos_get_customer_personal_relationships(
        session: Session,
        relationship_type: int,
        cif_id: str
):
    return session.execute(
        select(
            CustomerPersonalRelationship
        ).filter(
            CustomerPersonalRelationship.type == relationship_type,
            CustomerPersonalRelationship.customer_id == cif_id
        )).scalars().all()
