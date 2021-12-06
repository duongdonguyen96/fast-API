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
from app.utils.constant.cif import CONTACT_ADDRESS_CODE
from app.utils.error_messages import ERROR_CIF_NUMBER_NOT_EXIST
from app.utils.functions import dropdown

DETAIL_RELATIONSHIP_DATA = {
    "id": "1",
    "avatar_url": "https//example.com/example.jpg",
    "basic_information": {
        "cif_number": "1",
        "full_name_vn": "Nguyễn Anh Đào",
        "date_of_birth": "1990-08-12",
        "gender": {
            "id": "1",
            "code": "NU",
            "name": "Nữ"
        },
        "nationality": {
            "id": "1",
            "code": "VN",
            "name": "Việt Nam"
        },
        "telephone_number": "",
        "mobile_number": "0867589623",
        "email": "anhdao@gmail.com"
    },
    "identity_document": {
        "identity_number": "079190254791",
        "issued_date": "1990-12-08",
        "expired_date": "1990-12-08",
        "place_of_issue": {
            "id": "1",
            "code": "CAHCM",
            "name": "Công an TPHCM"
        }
    },
    "address_information": {
        "resident_address": {
            "number_and_street": "125 Võ Thị Sáu",
            "province": {
                "id": "1",
                "code": "HCM",
                "name": "Hồ Chí Minh"
            },
            "district": {
                "id": "3",
                "code": "Q3",
                "name": "Quận 3"
            },
            "ward": {
                "id": "8",
                "code": "P8",
                "name": "Phường 8"
            }
        },
        "contact_address": {
            "number_and_street": "120/6 Điện Biên Phủ",
            "province": {
                "id": "1",
                "code": "HCM",
                "name": "Hồ Chí Minh"
            },
            "district": {
                "id": "BT",
                "code": "BT",
                "name": "Quận Bình Thạnh"
            },
            "ward": {
                "id": "8",
                "code": "AP",
                "name": "Phường An Phước"
            }
        }
    }
}


async def repos_get_customer_detail(
        cif_number: str,
        session: Session
):
    customer = session.execute(
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
        .outerjoin(CustomerGender, CustomerIndividualInfo.gender_id == CustomerGender.id)
        .outerjoin(AddressCountry, Customer.nationality_id == AddressCountry.id)
        .outerjoin(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
        .outerjoin(PlaceOfIssue, CustomerIdentity.place_of_issue_id == PlaceOfIssue.id)
        .outerjoin(CustomerAddress, Customer.id == CustomerAddress.customer_id)
        .outerjoin(AddressProvince, CustomerAddress.address_province_id == AddressProvince.id)
        .outerjoin(AddressDistrict, CustomerAddress.address_district_id == AddressDistrict.id)
        .outerjoin(AddressWard, CustomerAddress.address_ward_id == AddressWard.id)
        .filter(
            Customer.cif_number == cif_number,
        )
    ).all()

    if not customer:
        return ReposReturn(
            is_error=True,
            msg=ERROR_CIF_NUMBER_NOT_EXIST,
            loc="cif_number"
        )

    # vì join với address bị lặp dữ liệu nên cần tạo dict địa chỉ dựa trên id để trả về
    customer_id__infos = {
        "customer": customer[0],
        "contact_address": None,
        "resident_address": None,
    }
    for customer in customer:
        address = {
            "province": dropdown(customer.AddressProvince),
            "district": dropdown(customer.AddressDistrict),
            "ward": dropdown(customer.AddressWard),
            "number_and_street": customer.CustomerAddress.address
        }
        if customer.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
            customer_id__infos["contact_address"] = address
        else:
            customer_id__infos["resident_address"] = address

    return ReposReturn(data={
        "id": customer_id__infos["customer"].id,
        "avatar_url": customer_id__infos["customer"].avatar_url,
        "basic_information": {
            "cif_number": customer_id__infos["customer"].cif_number,
            "full_name_vn": customer_id__infos["customer"].full_name_vn,
            "date_of_birth": customer_id__infos["customer"].CustomerIndividualInfo.date_of_birth,
            "gender": dropdown(customer_id__infos["customer"].CustomerGender),
            "nationality": dropdown(customer_id__infos["customer"].AddressCountry),
            "telephone_number": customer_id__infos["customer"].telephone_number,
            "mobile_number": customer_id__infos["customer"].mobile_number,
            "email": customer_id__infos["customer"].email,
        },
        "identity_document": {
            "identity_number": customer_id__infos["customer"].CustomerIdentity.identity_num,
            "issued_date": customer_id__infos["customer"].CustomerIdentity.issued_date,
            "place_of_issue": dropdown(customer_id__infos["customer"].PlaceOfIssue),
            "expired_date": customer_id__infos["customer"].CustomerIdentity.expired_date
        },
        "address_information": {
            "contact_address": customer_id__infos["contact_address"],
            "resident_address": customer_id__infos["resident_address"],
        }
    })


async def repos_get_customer_personal_relationships(
        session: Session,
        relationship_type: int,
        cif_id: str
):
    return session.execute(select(CustomerPersonalRelationship).filter(
        CustomerPersonalRelationship.type == relationship_type,
        CustomerPersonalRelationship.customer_id == cif_id
    )).scalars().all()
