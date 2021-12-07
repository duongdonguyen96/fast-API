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
from app.third_parties.oracle.models.cif.payment_account.model import (
    AgreementAuthorization, CasaAccount, JointAccountHolder
)
from app.third_parties.oracle.models.master_data.address import AddressCountry
from app.third_parties.oracle.models.master_data.customer import (
    CustomerGender, CustomerRelationshipType
)
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.utils.constant.cif import (
    CIF_ID_TEST, CONTACT_ADDRESS_CODE, IMAGE_TYPE_SIGNATURE,
    RESIDENT_ADDRESS_CODE
)
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
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
    # lấy dữ liệu các đồng sở hữu của tài khoản thanh toán theo cif_id
    account_holders = session.execute(
        select(
            JointAccountHolder
        ).join(
            CasaAccount,
            CasaAccount.id == JointAccountHolder.casa_account_id
        ).filter(CasaAccount.customer_id == cif_id)
    ).all()

    # lấy list cif_number trong account_holder
    list_cif_number = []
    for account_holder in account_holders:
        list_cif_number.append(account_holder.JointAccountHolder.cif_num)

    # lấy dữ liệu customer theo số cif_number
    customers = session.execute(
        select(
            Customer,
            AddressCountry,
            CustomerIdentity,
            CustomerIdentityImage,
            CustomerIndividualInfo,
            CustomerGender,
            PlaceOfIssue,
            CustomerPersonalRelationship,
            CustomerRelationshipType
        ).join(
            CustomerIdentity, Customer.id == CustomerIdentity.customer_id
        ).join(
            AddressCountry, Customer.nationality_id == AddressCountry.id
        ).join(
            PlaceOfIssue, CustomerIdentity.place_of_issue_id == PlaceOfIssue.id
        ).outerjoin(
            CustomerIndividualInfo, Customer.id == CustomerIndividualInfo.customer_id
        ).join(
            CustomerGender, CustomerIndividualInfo.gender_id == CustomerGender.id
        ).join(
            CustomerPersonalRelationship, Customer.id == CustomerPersonalRelationship.customer_id
        ).join(
            CustomerRelationshipType,
            CustomerRelationshipType.id == CustomerPersonalRelationship.customer_relationship_type_id
        ).join(
            CustomerIdentityImage, and_(
                CustomerIdentity.id == CustomerIdentityImage.identity_id,
                CustomerIdentityImage.image_type_id == IMAGE_TYPE_SIGNATURE
            )
        ).filter(Customer.cif_number.in_(list_cif_number))
    ).all()

    if not customers:
        return ReposReturn(is_error=True, msg='ERROR_CIF_NUMBER_NOT_EXIST', detail='')

    customer_address = session.execute(
        select(
            CustomerAddress,
        ).join(
            Customer, CustomerAddress.customer_id == Customer.id
        ).filter(Customer.cif_number.in_(list_cif_number))
    ).all()

    # lấy data address
    address_information = {}
    for row in customer_address:
        if row.CustomerAddress.customer_id not in address_information:
            address_information[row.CustomerAddress.customer_id] = {
                "content_address": None,
                "resident_address": None
            }

        if row.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
            address_information[row.CustomerAddress.customer_id]["content_address"] = row.CustomerAddress.address

        if row.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
            address_information[row.CustomerAddress.customer_id]["resident_address"] = row.CustomerAddress.address

    # lấy data customer
    address = None
    signature = None
    customer__signature = {}
    account__holder = {}
    for customer in customers:
        if not customer.CustomerIndividualInfo:
            return ReposReturn(is_error=True, msg='CUSTOMER_INDIVIDUAL_INFO', detail=f'{customer.Customer.id}')

        if not customer.CustomerIdentity:
            return ReposReturn(is_error=True, msg='CUSTOMER_IDENTITY', detail=f'{customer.Customer.id}')
        # gán lại giá trị cho address
        for key, values in address_information.items():
            if customer.Customer.id == key:
                address = values

        if not customer.CustomerIdentityImage:
            return ReposReturn(is_error=True, msg='CUSTOMER_IDENTITY_IMAGE', detail=f'{customer.Customer.id}')
        # lấy danh sách chữ ký theo từng customer_id
        if customer.Customer.id not in customer__signature:
            customer__signature[customer.Customer.id] = []

        customer__signature[customer.Customer.id].append({
            "id": customer.CustomerIdentityImage.id,
            "image_url": customer.CustomerIdentityImage.image_url
        })
        # gán giá trị cho chứ ký
        for key, values in customer__signature.items():
            if customer.Customer.id == key:
                signature = values

        # lấy giá trị customer_account_holder theo customer_id
        if customer.Customer.id not in account__holder:
            account__holder[customer.Customer.id] = {}

            account__holder[customer.Customer.id].update(**{
                "id": customer.Customer.id,
                "full_name_vn": customer.Customer.full_name_vn,
                "basic_information": {
                    "cif_number": customer.Customer.cif_number,
                    "full_name_vn": customer.Customer.full_name_vn,
                    "customer_relationship": dropdown(customer.CustomerRelationshipType),
                    "date_of_birth": customer.CustomerIndividualInfo.date_of_birth,
                    "gender": dropdown(customer.CustomerGender),
                    "nationality": dropdown(customer.AddressCountry),
                    "mobile_number": customer.Customer.mobile_number,
                    "signature": signature
                },
                "identity_document": {
                    "identity_number": customer.CustomerIdentity.identity_num,
                    "issued_date": customer.CustomerIdentity.issued_date,
                    "expired_date": customer.CustomerIdentity.expired_date,
                    "place_of_issue": dropdown(customer.PlaceOfIssue)
                },
                "address_information": address,
            })

    agreement_authorizations = session.execute(
        select(
            AgreementAuthorization
        )
    ).scalars()

    if not agreement_authorizations:
        return ReposReturn(is_error=True, msg='AGREEMENT_AUTHORIZATIONS_NOT_EXIST', detail='agreement_authorizations')

    agreement_authorization = [{
        "id": agreement_authorization.id,
        "code": agreement_authorization.code,
        "name": agreement_authorization.name,
        "active_flag": agreement_authorization.active_flag,
    } for agreement_authorization in agreement_authorizations]

    response_data = {
        "joint_account_holder_flag": account_holders[0].JointAccountHolder.joint_account_holder_flag,
        "number_of_joint_account_holder": len(account_holders),
        "joint_account_holders": [customer for customer in account__holder.values()],
        "agreement_authorization": agreement_authorization
    }

    return ReposReturn(data=response_data)


async def repos_detail_co_owner(cif_id: str, cif_number_need_to_find: str):
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    return ReposReturn(data={
        "id": "1",
        "basic_information": {
            "full_name_vn": "TRẦN NGỌC AN",
            "cif_number": "0298472",
            "customer_relationship": {
                "id": "1",
                "code": "code",
                "name": "Chị gái"
            },
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
    })
