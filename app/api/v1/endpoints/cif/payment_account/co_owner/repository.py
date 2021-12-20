import json
from typing import List

from sqlalchemy import and_, delete, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.repository import (
    write_transaction_log_and_update_booking
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
    IMAGE_TYPE_CODE_SIGNATURE, IMAGE_TYPE_SIGNATURE
)
from app.utils.error_messages import (
    ERROR_AGREEMENT_AUTHORIZATIONS_NOT_EXIST, ERROR_CASA_ACCOUNT_NOT_EXIST,
    ERROR_CIF_NUMBER_EXIST
)
from app.utils.functions import now


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
    if not casa_account:
        return ReposReturn(is_error=True, msg=ERROR_CASA_ACCOUNT_NOT_EXIST, loc=f"cif_id: {cif_id}")
    return ReposReturn(data=casa_account)


@auto_commit
async def repos_save_co_owner(
        cif_id: str,
        save_account_holder: list,
        save_account_agree: list,
        log_data: json,
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

    await write_transaction_log_and_update_booking(
        description="Tạo CIF -> Tài khoản thanh toán -> Thông tin đồng sở hữu -- Tạo mới",
        log_data=log_data,
        session=session,
        customer_id=cif_id
    )

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
    detail_co_owner = session.execute(
        select(
            Customer,
            CustomerIdentity,
            CustomerIndividualInfo,
            CustomerIdentityImage,
            AddressCountry,
            CustomerAddress,
            CustomerGender,
            PlaceOfIssue,
            CustomerIdentityType,
            CustomerPersonalRelationship,
            CustomerRelationshipType
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
            CustomerPersonalRelationship,
            CustomerPersonalRelationship.customer_personal_relationship_cif_number == cif_number_need_to_find
        ).join(
            CustomerIdentityType, CustomerIdentity.identity_type_id == CustomerIdentityType.id
        ).join(
            CustomerRelationshipType,
            CustomerPersonalRelationship.customer_relationship_type_id == CustomerRelationshipType.id
        ).join(
            CustomerAddress, CustomerAddress.customer_id == Customer.id
        ).filter(Customer.cif_number == cif_number_need_to_find)
    ).all()

    if not detail_co_owner:
        return detail_co_owner(is_error=True, msg=ERROR_CIF_NUMBER_EXIST, loc='cif_number')

    return ReposReturn(data=detail_co_owner)
