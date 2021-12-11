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
    ERROR_CIF_NUMBER_EXIST, ERROR_CUSTOMER_IDENTITY,
    ERROR_CUSTOMER_IDENTITY_IMAGE, ERROR_CUSTOMER_INDIVIDUAL_INFO
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

    # check account_holder
    if not account_holders:
        return ReposReturn(is_error=True, msg=ERROR_CASA_ACCOUNT_NOT_EXIST, loc='cif_id')

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
                "contact_address": None,
                "resident_address": None
            }

        if row.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
            address_information[row.CustomerAddress.customer_id]["contact_address"] = row.CustomerAddress.address

        if row.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
            address_information[row.CustomerAddress.customer_id]["resident_address"] = row.CustomerAddress.address

    # lấy data customer
    address = None
    signature = None
    customer__signature = {}
    account__holder = {}
    for customer in customers:
        if not customer.CustomerIndividualInfo:
            return ReposReturn(is_error=True, msg=ERROR_CUSTOMER_INDIVIDUAL_INFO, loc=f'{customer.Customer.id}')

        if not customer.CustomerIdentity:
            return ReposReturn(is_error=True, msg=ERROR_CUSTOMER_IDENTITY, loc=f'{customer.Customer.id}')
        # gán lại giá trị cho address
        for key, values in address_information.items():
            if customer.Customer.id == key:
                address = values

        if not customer.CustomerIdentityImage:
            return ReposReturn(is_error=True, msg=ERROR_CUSTOMER_IDENTITY_IMAGE, loc=f'{customer.Customer.id}')
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
                    "identity_type": dropdown(customer.CustomerIdentityType),
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
        return ReposReturn(is_error=True, msg=ERROR_AGREEMENT_AUTHORIZATIONS_NOT_EXIST, loc='agreement_authorizations')

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
