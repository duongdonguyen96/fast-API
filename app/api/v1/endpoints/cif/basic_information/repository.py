from typing import List, Set

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.identity import (
    CustomerSubIdentityType, PlaceOfIssue
)
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST

DETAIL_RELATIONSHIP_DATA = {
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


async def repos_detail_relationship(cif_id: str, cif_number_need_to_find: str):
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    return ReposReturn(data=DETAIL_RELATIONSHIP_DATA)


async def repos_get_identity_document_types(sub_identity_type_ids: List[str], session: Session):
    crm_sub_identity_types = session.execute(
        select(
            CustomerSubIdentityType
        ).filter(CustomerSubIdentityType.code.in_(sub_identity_type_ids))
    ).scalars().all()

    if len(crm_sub_identity_types) != len(sub_identity_type_ids):
        return ReposReturn(is_error=True, detail="Sub Identity Type is not exist", loc="sub_identity_type_id")

    return ReposReturn(data=crm_sub_identity_types)


async def repos_get_place_of_issue(place_of_issue_ids: Set[str], session: Session):
    crm_place_of_issues = session.execute(
        select(
            PlaceOfIssue
        ).filter(PlaceOfIssue.id.in_(place_of_issue_ids))
    ).scalars().all()

    if len(crm_place_of_issues) != len(place_of_issue_ids):
        return ReposReturn(is_error=True, detail="Place Of Issue is not exist", loc="place_of_issue_id")

    return ReposReturn(data=crm_place_of_issues)
