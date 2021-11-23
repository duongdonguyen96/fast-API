from typing import Union

from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.schema_request import (
    CitizenCardSaveRequest, IdentityCardSaveRequest, PassportSaveRequest
)
from app.api.v1.endpoints.cif.repository import repos_get_identity_info
from app.third_parties.oracle.models.cif.basic_information.contact.model import CustomerAddress
from app.third_parties.oracle.models.cif.basic_information.identity.model import CustomerIdentity, \
    CustomerIdentityImage, CustomerCompareImage
from app.third_parties.oracle.models.cif.basic_information.model import Customer
from app.third_parties.oracle.models.cif.basic_information.personal.model import CustomerIndividualInfo
from app.third_parties.oracle.models.master_data.address import AddressProvince, AddressCountry, AddressDistrict, \
    AddressWard
from app.third_parties.oracle.models.master_data.customer import CustomerGender
from app.third_parties.oracle.models.master_data.identity import CustomerIdentityType, PlaceOfIssue, HandSide, \
    FingerType, PassportType, PassportCode
from app.third_parties.oracle.models.master_data.others import Nation, Religion
from app.utils.constant.cif import (
    CIF_ID_TEST, IDENTITY_DOCUMENT_TYPE
)
from app.utils.error_messages import (
    ERROR_CIF_ID_NOT_EXIST, ERROR_IDENTITY_DOCUMENT_NOT_EXIST, MESSAGE_STATUS
)
from app.utils.functions import now

IDENTITY_LOGS_INFO = [
    {
        "reference_flag": True,
        "created_date": "2021-02-18",
        "identity_document_type": {
            "id": "1",
            "code": "CMND",
            "name": "Chứng minh nhân dân"
        },
        "identity_images": [
            {
                "image_url": "https://example.com/example.jpg"
            },
            {
                "image_url": "https://example.com/example.jpg"
            }
        ]
    },
    {
        "reference_flag": False,
        "created_date": "2021-02-18",
        "identity_document_type": {
            "id": "2",
            "code": "CCCD",
            "name": "Căn cước công dân"
        },
        "identity_images": [
            {
                "image_url": "https://example.com/example.jpg"
            },
            {
                "image_url": "https://example.com/example.jpg"
            }
        ]
    },
    {
        "reference_flag": False,
        "created_date": "2021-02-18",
        "identity_document_type": {
            "id": "3",
            "code": "HC",
            "name": "Hộ chiếu"
        },
        "identity_images": [
            {
                "image_url": "https://example.com/example.jpg"
            }
        ]
    }
]


async def repos_get_detail_identity(
        cif_id: str, identity_document_type_id: str, session: Session
) -> ReposReturn:
    if identity_document_type_id not in IDENTITY_DOCUMENT_TYPE:
        return ReposReturn(is_error=True, msg=f"{MESSAGE_STATUS[ERROR_IDENTITY_DOCUMENT_NOT_EXIST]} in "
                                              f"{IDENTITY_DOCUMENT_TYPE}", loc='identity_document_type_id')

    identities = session.execute(
        select(
            Customer,
            CustomerIdentity,
            CustomerIndividualInfo,
            CustomerAddress,
            CustomerIdentityImage,
            CustomerIdentityType,
            CustomerCompareImage,
            HandSide,
            FingerType,
            PlaceOfIssue,
            CustomerGender,
            AddressCountry,
            AddressProvince,
            AddressDistrict,
            AddressWard,
            Nation,
            Religion,
            PassportType,
            PassportCode
        )
        .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
        .join(CustomerIndividualInfo, Customer.id == CustomerIndividualInfo.customer_id)
        .join(CustomerAddress, Customer.id == CustomerAddress.customer_id)
        .outerjoin(CustomerIdentityImage, CustomerIdentity.id == CustomerIdentityImage.identity_id)
        .outerjoin(CustomerCompareImage, CustomerIdentityImage.id == CustomerCompareImage.identity_image_id)
        .outerjoin(CustomerIdentityType, CustomerIdentity.identity_type_id == CustomerIdentityType.id)

        .outerjoin(HandSide, CustomerIdentityImage.hand_side_id == HandSide.id)
        .outerjoin(FingerType, CustomerIdentityImage.finger_type_id == FingerType.id)
        .join(PlaceOfIssue, CustomerIdentity.place_of_issue_id == PlaceOfIssue.id)
        .join(CustomerGender, CustomerIndividualInfo.gender_id == CustomerGender.id)
        .join(AddressCountry, CustomerIndividualInfo.country_of_birth_id == AddressCountry.id)
        .join(AddressProvince, CustomerIndividualInfo.place_of_birth_id == AddressProvince.id)
        .join(AddressDistrict, CustomerAddress.address_district_id == AddressDistrict.id)
        .join(AddressWard, CustomerAddress.address_ward_id == AddressWard.id)
        .join(Nation, CustomerIndividualInfo.nation_id == Nation.id)
        .join(Religion, CustomerIndividualInfo.religion_id == Religion.id)
        .outerjoin(PassportType, CustomerIdentity.passport_type_id == PassportType.id)
        .outerjoin(PassportCode, CustomerIdentity.passport_code_id == PassportCode.id)
        .filter(
            Customer.id == cif_id,
            CustomerIdentity.identity_type_id == identity_document_type_id
        )
        .order_by(desc(CustomerIdentityImage.updater_at))
    ).all()

    if not identities:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    identity_info = await repos_get_identity_info(identities, identity_document_type_id)

    return ReposReturn(data=identity_info)


async def repos_get_list_log(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=IDENTITY_LOGS_INFO)


async def repos_save(
        identity_document_req: Union[IdentityCardSaveRequest, CitizenCardSaveRequest, PassportSaveRequest],
        created_by: str
):
    identity_document_type_id = identity_document_req.identity_document_type.id
    if identity_document_type_id not in IDENTITY_DOCUMENT_TYPE:
        return ReposReturn(is_error=True, msg=ERROR_IDENTITY_DOCUMENT_NOT_EXIST, loc='identity_document_type -> id')

    return ReposReturn(data={
        "cif_id": identity_document_req.cif_id,
        "created_at": now(),
        "created_by": created_by
    })
