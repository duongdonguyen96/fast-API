from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.cif.payment_account.co_owner.schema import (
    AccountHolderRequest
)
from app.third_parties.oracle.models.cif.basic_information.contact.model import (
    CustomerAddress
)
from app.third_parties.oracle.models.cif.basic_information.guardian_and_relationship.model import (
    CustomerPersonalRelationship
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity, CustomerIdentityImage
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.basic_information.personal.model import (
    CustomerIndividualInfo
)
from app.third_parties.oracle.models.master_data.address import AddressCountry
from app.third_parties.oracle.models.master_data.customer import (
    CustomerGender, CustomerRelationshipType
)
from app.third_parties.oracle.models.master_data.identity import (
    CustomerIdentityType, PlaceOfIssue
)
from app.utils.constant.cif import (
    CIF_ID_TEST, CONTACT_ADDRESS_CODE, IMAGE_TYPE_CODE_SIGNATURE,
    RESIDENT_ADDRESS_CODE
)
from app.utils.error_messages import (
    ERROR_CIF_ID_NOT_EXIST, ERROR_CIF_NUMBER_EXIST
)
from app.utils.functions import dropdown, now


async def repos_save_co_owner(cif_id: str, co_owner: AccountHolderRequest, created_by: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_get_co_owner_data(cif_id: str, session: Session) -> ReposReturn:
    # query_data = session.execute(
    #     select(
    #         Customer,
    #         CasaAccount,
    #         JointAccountHolder
    #     ).join(
    #         CasaAccount, Customer.id == CasaAccount.customer_id
    #     ).join(
    #         JointAccountHolder, CasaAccount.id == JointAccountHolder.casa_account_id
    #     ).filter(Customer.id == cif_id)
    # ).all()
    #
    # first_row = query_data[0]
    #
    # data = {
    #     "joint_account_holder_flag":first_row.JointAccountHolder.joint_account_holder_flag,
    # }

    # return ReposReturn(data=data)
    return ReposReturn(data={
        "joint_account_holder_flag": True,
        "number_of_joint_account_holder": 3,
        "joint_account_holders": [
            {
                "id": "1",
                "full_name_vn": "Trần Ngọc An",
                "basic_information": {
                    "cif_number": "0298472",
                    "customer_relationship": {
                        "id": "1",
                        "code": "code",
                        "name": "Chị gái"
                    },
                    "full_name_vn": "TRẦN NGỌC AN",
                    "date_of_birth": "1990-02-20",
                    "gender": {
                        "id": "1",
                        "code": "Code",
                        "name": "Nữ"
                    },
                    "nationality": {
                        "id": "1",
                        "code": "Code",
                        "name": "Việt Nam"
                    },
                    "mobile_number": "08675968221",
                    "signature_1": {
                        "id": "1",
                        "code": "code",
                        "name": "mẫu chứ ký 1",
                        "image_url": "https://example.com/abc.png"
                    },
                    "signature_2": {
                        "id": "2",
                        "code": "code",
                        "name": "mẫu chứ ký 2",
                        "image_url": "https://example.com/abc.png"
                    }
                },
                "identity_document": {
                    "identity_number": "254136582",
                    "issued_date": "1990-02-20",
                    "expired_date": "1990-02-20",
                    "place_of_issue": {
                        "id": "1",
                        "code": "code",
                        "name": "TP. Hồ Chí Minh"
                    }
                },
                "address_information": {
                    "content_address": "48 Phó Cơ Điều, Phường 12, Quận 5, Thành phố Hồ Chí Minh",
                    "resident_address": "6, Q.6, 279 Lê Quang Sung, Phường 6, Quận 6, Thành phố Hồ Chí Minh"
                }
            }
        ],
        "agreement_authorization": [
            {
                "id": "1",
                "code": "code",
                "content": "Rút tiền (tiền mặt/chuyển khoản) tại quầy; Đề nghị SCB cung "
                           "ứng Séc trắng và nhận Séc trắng tại SCB; Phát hành Séc;"
                           " Đóng tài khoản (bao gồm Thẻ ghi Nợ và dịch vụ Ngân hàng điện tử kết nối với tài khoản)"
                           " và xử lý số dư sau khi đóng tài khoản; Xác nhận số dư tài khoản; "
                           "Tạm khóa/Phong tỏa tài khoản; Đề nghị SCB phát hành Thẻ ghi Nợ kết nối với "
                           "tài khoản thanh toán chung tại SCB.",
                "agreement_flag": True,
                "method_sign": {
                    "id": "1",
                    "code": "code",
                    "name": "Phương thức 3"
                },
                "signature_list": [
                    {
                        "id": "1",
                        "full_name_vn": "Nguyễn Anh Đào"
                    },
                    {
                        "id": "2",
                        "full_name_vn": "Lê Văn A"
                    }
                ]
            },
            {
                "id": "2",
                "code": "code2",
                "content": "Giao dịch chấm dứt tạm khóa, chấm dứt phong tỏa tài khoản và các giao dịch phát sinh khác "
                           "ngoài nội dung nêu tại Nội dung 1: Chữ ký của tất cả các đồng chủ tài khoản.",
                "agreement_flag": True,
                "method_sign": {
                    "id": "1",
                    "code": "code",
                    "name": "Phương thức 2"
                },
                "signature_list": []
            }
        ]
    })


async def repos_detail_co_owner(cif_id: str, cif_number_need_to_find: str, session: Session):
    customer = session.execute(
        select(
            Customer,
            CustomerIdentity,
            CustomerIndividualInfo,
            CustomerIdentityImage,
            AddressCountry,
            CustomerGender,
            PlaceOfIssue,
            CustomerIdentityType
        ).join(
            CustomerIdentity, CustomerIdentity.customer_id == Customer.id
        ).join(
            CustomerIndividualInfo, CustomerIndividualInfo.customer_id == Customer.id
        ).join(
            CustomerIdentityImage, and_(
                CustomerIdentity.id == CustomerIdentityImage.identity_id,
                CustomerIdentityImage.image_type_id == IMAGE_TYPE_CODE_SIGNATURE
            )
        ).join(
            AddressCountry, Customer.nationality_id == AddressCountry.id
        ).join(
            CustomerGender, CustomerIndividualInfo.gender_id == CustomerGender.id
        ).join(
            PlaceOfIssue, CustomerIdentity.place_of_issue_id == PlaceOfIssue.id
        ).join(
            CustomerIdentityType, CustomerIdentity.identity_type_id == CustomerIdentityType.id
        ).filter(Customer.cif_number == cif_number_need_to_find)
    ).all()

    if not customer:
        return ReposReturn(is_error=True, msg=ERROR_CIF_NUMBER_EXIST, loc='cif_number')

    relationship = session.execute(
        select(
            CustomerRelationshipType
        ).join(
            CustomerPersonalRelationship,
            CustomerPersonalRelationship.customer_relationship_type_id == CustomerRelationshipType.id
        ).filter(
            CustomerPersonalRelationship.customer_personal_relationship_cif_number == cif_number_need_to_find
        )
    ).scalar()

    customer_address = session.execute(
        select(
            Customer,
            CustomerAddress
        ).join(
            CustomerAddress, CustomerAddress.customer_id == Customer.id
        ).filter(Customer.cif_number == cif_number_need_to_find)
    ).all()

    if not customer_address:
        return ReposReturn(is_error=True, msg=ERROR_CIF_NUMBER_EXIST, loc='cif_number')

    resident_address = None
    contact_address = None

    for row in customer_address:
        if row.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
            resident_address = row.CustomerAddress.address
        if row.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
            contact_address = row.CustomerAddress.address

    first_row = customer[0]

    response_data = {
        "id": first_row.Customer.id,
        "basic_information": {},
        "identity_document": {},
        "address_information": {
            'contact_address': contact_address,
            'resident_address': resident_address
        }
    }

    response_data['basic_information'].update(**{
        "full_name_vn": first_row.Customer.full_name_vn,
        "cif_number": first_row.Customer.cif_number,
        "date_of_birth": first_row.CustomerIndividualInfo.date_of_birth,
        "customer_relationship": dropdown(relationship),
        "nationality": dropdown(first_row.AddressCountry),
        "gender": dropdown(first_row.CustomerGender),
        "mobile_number": first_row.Customer.mobile_number,
        "signature_1": {
            "id": first_row.CustomerIdentityImage.id,
            "image_url": first_row.CustomerIdentityImage.image_url
        },
        "signature_2": {
            "id": customer[1].CustomerIdentityImage.id,
            "image_url": customer[1].CustomerIdentityImage.image_url
        },
    })

    response_data['identity_document'].update(**{
        "identity_number": first_row.CustomerIdentity.identity_num,
        "identity_type": dropdown(first_row.CustomerIdentityType),
        "issued_date": first_row.CustomerIdentity.issued_date,
        "expired_date": first_row.CustomerIdentity.expired_date,
        "place_of_issue": dropdown(first_row.PlaceOfIssue)
    })

    return ReposReturn(data=response_data)
