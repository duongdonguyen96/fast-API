from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
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
from app.third_parties.oracle.models.master_data.customer import (
    CustomerGender, CustomerRelationshipType
)
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.utils.constant.cif import (
    CONTACT_ADDRESS_CODE, CUSTOMER_RELATIONSHIP_TYPE_GUARDIAN
)
from app.utils.functions import dropdown, now

GUARDIAN_INFO_DETAIL = {
    "guardian_flag": True,
    "number_of_guardian": 1,
    "guardians": [
        {
            "id": "1",
            "avatar_url": "https//example.com/example.jpg",
            "basic_information": {
                "cif_number": "1",
                "customer_relationship": {
                    "id": "1",
                    "code": "MOTHER",
                    "name": "Mẹ"
                },
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
    ]
}


async def repos_get_guardians(
        cif_id: str,
        session: Session,
):
    guardians = session.execute(
        select(
            CustomerPersonalRelationship,
            CustomerRelationshipType,
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
        .join(Customer, CustomerPersonalRelationship.customer_relationship_id == Customer.id)
        .join(CustomerIndividualInfo, Customer.id == CustomerIndividualInfo.customer_id)
        .join(CustomerRelationshipType,
              CustomerPersonalRelationship.customer_relationship_type_id == CustomerRelationshipType.id)
        .outerjoin(CustomerGender, CustomerIndividualInfo.gender_id == CustomerGender.id)
        .outerjoin(AddressCountry, Customer.nationality_id == AddressCountry.id)
        .outerjoin(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
        .outerjoin(PlaceOfIssue, CustomerIdentity.place_of_issue_id == PlaceOfIssue.id)
        .outerjoin(CustomerAddress, Customer.id == CustomerAddress.customer_id)
        .outerjoin(AddressProvince, CustomerAddress.address_province_id == AddressProvince.id)
        .outerjoin(AddressDistrict, CustomerAddress.address_district_id == AddressDistrict.id)
        .outerjoin(AddressWard, CustomerAddress.address_ward_id == AddressWard.id)
        .filter(
            CustomerPersonalRelationship.customer_id == cif_id,
            CustomerPersonalRelationship.type == CUSTOMER_RELATIONSHIP_TYPE_GUARDIAN,
        )
    ).all()

    # vì join với address bị lặp dữ liệu nên cần tạo dict địa chỉ dựa trên id để trả về
    guardian_id__infos = {}
    for guardian in guardians:
        if not guardian_id__infos.get(guardian.id):
            guardian_id__infos[guardian.id] = {
                "guardian": guardian,
                "contact_address": None,
                "resident_address": None,
            }
        address = {
            "province": dropdown(guardian.AddressProvince),
            "district": dropdown(guardian.AddressDistrict),
            "ward": dropdown(guardian.AddressWard),
            "number_and_street": guardian.CustomerAddress.address
        }
        if guardian.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
            guardian_id__infos[guardian.id]["contact_address"] = address
        else:
            guardian_id__infos[guardian.id]["resident_address"] = address

    return ReposReturn(data={
        "guardian_flag": True if guardian_id__infos else False,
        "number_of_guardian": len(guardian_id__infos),
        "guardians": [{
            "id": info["guardian"].id,
            "avatar_url": info["guardian"].avatar_url,
            "basic_information": {
                "cif_number": info["guardian"].cif_number,
                "customer_relationship": dropdown(info["guardian"].CustomerRelationshipType),
                "full_name_vn": info["guardian"].full_name_vn,
                "date_of_birth": info["guardian"].CustomerIndividualInfo.date_of_birth,
                "gender": dropdown(info["guardian"].CustomerGender),
                "nationality": dropdown(info["guardian"].AddressCountry),
                "telephone_number": info["guardian"].telephone_number,
                "mobile_number": info["guardian"].mobile_number,
                "email": info["guardian"].email,
            },
            "identity_document": {
                "identity_number": info["guardian"].CustomerIdentity.identity_num,
                "issued_date": info["guardian"].CustomerIdentity.issued_date,
                "place_of_issue": dropdown(info["guardian"].PlaceOfIssue),
                "expired_date": info["guardian"].CustomerIdentity.expired_date
            },
            "address_information": {
                "contact_address": info["contact_address"],
                "resident_address": info["resident_address"],
            }
        } for info in guardian_id__infos.values()]
    })


@auto_commit
async def repos_save_guardians(
        cif_id: str,
        list_data_insert: list,
        created_by: str,
        session: Session,
        relationship_type: int = CUSTOMER_RELATIONSHIP_TYPE_GUARDIAN
):
    # clear old data
    session.execute(delete(
        CustomerPersonalRelationship
    ).filter(
        CustomerPersonalRelationship.customer_id == cif_id,
        CustomerPersonalRelationship.type == relationship_type
    ))

    data_insert = [CustomerPersonalRelationship(**guardian) for guardian in list_data_insert]

    session.bulk_save_objects(data_insert)

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })
