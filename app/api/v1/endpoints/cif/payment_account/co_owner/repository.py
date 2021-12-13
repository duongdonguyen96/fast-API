from typing import List

from sqlalchemy import and_, delete, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
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
    AgreementAuthorization, CasaAccount, JointAccountHolder,
    JointAccountHolderAgreementAuthorization
)
from app.third_parties.oracle.models.master_data.address import AddressCountry
from app.third_parties.oracle.models.master_data.customer import (
    CustomerGender, CustomerRelationshipType
)
from app.third_parties.oracle.models.master_data.identity import (
    CustomerIdentityType, PlaceOfIssue
)
from app.utils.constant.cif import (
    CONTACT_ADDRESS_CODE, IMAGE_TYPE_CODE_SIGNATURE, IMAGE_TYPE_SIGNATURE,
    RESIDENT_ADDRESS_CODE
)
from app.utils.error_messages import (
    ERROR_AGREEMENT_AUTHORIZATIONS_NOT_EXIST, ERROR_CASA_ACCOUNT_NOT_EXIST,
    ERROR_CIF_NUMBER_EXIST
)
from app.utils.functions import dropdown, now


async def repos_check_list_cif_number(list_cif_number_request: list, session: Session) -> ReposReturn:
    list_customer = session.execute(
        select(
            Customer
        ).filter(Customer.cif_number.in_(list_cif_number_request))
    ).all()

    if not list_customer:
        return ReposReturn(is_error=True, msg='CIF_NUMBER_NOT_EXIT')

    return ReposReturn(data=list_customer)


async def repos_get_casa_account(cif_id: str, session: Session) -> ReposReturn:
    casa_account = session.execute(
        select(
            CasaAccount.id
        ).filter(CasaAccount.customer_id == cif_id)
    ).scalar()

    return ReposReturn(data=casa_account)


@auto_commit
async def repos_save_co_owner(
        cif_id: str,
        save_account_holder: List,
        save_account_agree: List,
        session: Session,
        created_by: str
) -> ReposReturn:
    # lấy danh sách account holder để xóa
    account_holder_ids = session.execute(
        select(
            JointAccountHolder.id
        ).join(
            CasaAccount, and_(
                JointAccountHolder.casa_account_id == CasaAccount.id,
                CasaAccount.customer_id == cif_id
            )
        )
    ).scalars().all()

    # xóa JointAccountHolderAgreementAuthorization
    session.execute(
        delete(
            JointAccountHolderAgreementAuthorization
        ).filter(
            JointAccountHolderAgreementAuthorization.joint_account_holder_id.in_(account_holder_ids)
        )
    )

    # xóa account holder
    session.execute(
        delete(
            JointAccountHolder
        ).filter(JointAccountHolder.id.in_(account_holder_ids))
    )

    session.bulk_save_objects([JointAccountHolder(**data_insert) for data_insert in save_account_holder])

    session.bulk_save_objects(
        [JointAccountHolderAgreementAuthorization(**data_insert) for data_insert in save_account_agree])

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_get_list_cif_number(cif_id: str, session: Session):
    # lấy dữ liệu các đồng sở hữu của tài khoản thanh toán theo cif_id
    account_holders = session.execute(
        select(
            JointAccountHolder
        ).join(
            CasaAccount,
            CasaAccount.id == JointAccountHolder.casa_account_id
        ).filter(CasaAccount.customer_id == cif_id)
    ).all()

    # check account_holder
    if not account_holders:
        return ReposReturn(is_error=True, msg=ERROR_CASA_ACCOUNT_NOT_EXIST, loc='cif_id')

    # lấy list cif_number trong account_holder
    list_cif_number = []
    for account_holder in account_holders:
        list_cif_number.append(account_holder.JointAccountHolder.cif_num)

    return account_holders, list_cif_number


async def repos_get_customer_by_cif_number(list_cif_number: List[str], session: Session) -> ReposReturn:
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
            CustomerIdentityType,
            CustomerPersonalRelationship,
            CustomerRelationshipType
        ).join(
            CustomerIdentity, Customer.id == CustomerIdentity.customer_id
        ).join(
            AddressCountry, Customer.nationality_id == AddressCountry.id
        ).join(
            PlaceOfIssue, CustomerIdentity.place_of_issue_id == PlaceOfIssue.id
        ).join(
            CustomerIndividualInfo, Customer.id == CustomerIndividualInfo.customer_id
        ).join(
            CustomerIdentityType, CustomerIdentity.identity_type_id == CustomerIdentityType.id
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
        return ReposReturn(is_error=True, msg=ERROR_CIF_NUMBER_EXIST, loc='cif_number')

    return ReposReturn(data=customers)


async def repos_get_customer_address(list_cif_number: List[str], session: Session) -> ReposReturn:
    customer_address = session.execute(
        select(
            CustomerAddress,
        ).join(
            Customer, CustomerAddress.customer_id == Customer.id
        ).filter(Customer.cif_number.in_(list_cif_number))
    ).all()

    return ReposReturn(data=customer_address)


async def repos_get_agreement_authorizations(session: Session) -> ReposReturn:
    agreement_authorizations = session.execute(
        select(
            AgreementAuthorization
        )
    ).scalars()

    if not agreement_authorizations:
        return ReposReturn(is_error=True, msg=ERROR_AGREEMENT_AUTHORIZATIONS_NOT_EXIST, loc='agreement_authorizations')

    return ReposReturn(data=agreement_authorizations)


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
    customer__signature = {}
    for signature in customer:
        if signature.Customer.id not in customer__signature:
            customer__signature[signature.Customer.id] = []
        customer__signature[signature.Customer.id].append({
            'id': signature.CustomerIdentityImage.id,
            'image_url': signature.CustomerIdentityImage.image_url
        })

    signature = None
    for customer_signature in customer__signature.values():
        signature = customer_signature

    response_data['basic_information'].update(**{
        "full_name_vn": first_row.Customer.full_name_vn,
        "cif_number": first_row.Customer.cif_number,
        "date_of_birth": first_row.CustomerIndividualInfo.date_of_birth,
        "customer_relationship": dropdown(relationship),
        "nationality": dropdown(first_row.AddressCountry),
        "gender": dropdown(first_row.CustomerGender),
        "mobile_number": first_row.Customer.mobile_number,
        "signature": signature
    })

    response_data['identity_document'].update(**{
        "identity_number": first_row.CustomerIdentity.identity_num,
        "identity_type": dropdown(first_row.CustomerIdentityType),
        "issued_date": first_row.CustomerIdentity.issued_date,
        "expired_date": first_row.CustomerIdentity.expired_date,
        "place_of_issue": dropdown(first_row.PlaceOfIssue)
    })

    return ReposReturn(data=response_data)
