import json

from sqlalchemy import and_, select, update
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.repository import (
    write_transaction_log_and_update_booking
)
from app.third_parties.oracle.models.cif.basic_information.contact.model import (
    CustomerAddress, CustomerProfessional
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.others import (
    AverageIncomeAmount, Career, Position
)
from app.utils.constant.cif import CONTACT_ADDRESS_CODE, RESIDENT_ADDRESS_CODE
from app.utils.functions import dropdown


async def repos_get_detail_contact_information(cif_id: str, session: Session) -> ReposReturn:
    customer_addresses = session.execute(
        select(
            CustomerAddress,
            AddressCountry,
            AddressProvince,
            AddressDistrict,
            AddressWard,
            CustomerProfessional,
            Career,
            AverageIncomeAmount,
            Position
        )
        .join(Customer, CustomerAddress.customer_id == Customer.id)
        .join(CustomerProfessional, Customer.customer_professional_id == CustomerProfessional.id)
        .join(AddressCountry, CustomerAddress.address_country_id == AddressCountry.id)
        .join(AddressProvince, CustomerAddress.address_province_id == AddressProvince.id)
        .join(AddressDistrict, CustomerAddress.address_district_id == AddressDistrict.id)
        .outerjoin(AddressWard, CustomerAddress.address_ward_id == AddressWard.id)
        .join(Career, CustomerProfessional.career_id == Career.id)
        .join(AverageIncomeAmount, CustomerProfessional.average_income_amount_id == AverageIncomeAmount.id)
        .join(Position, CustomerProfessional.position_id == Position.id)
        .filter(
            Customer.id == cif_id
        )
    ).all()

    domestic_contact_information_detail = {
        "resident_address": {}
    }
    for customer_address, address_country, address_province, address_district, address_ward, \
            _, _, _, _ in customer_addresses:

        if customer_address.address_type_id == RESIDENT_ADDRESS_CODE:
            if customer_address.address_domestic_flag:
                domestic_contact_information_detail["resident_address"].update({
                    "domestic_address": {
                        "country": dropdown(address_country),
                        "province": dropdown(address_province),
                        "district": dropdown(address_district),
                        "ward": dropdown(address_ward),
                        "number_and_street": customer_address.address
                    },
                    "foreign_address": None
                })
            else:
                domestic_contact_information_detail["resident_address"].update({
                    "domestic_address": None,
                    "foreign_address": {
                        "country": dropdown(address_country),
                        "address_1": customer_address.address,
                        "address_2": customer_address.address_2,
                        "province": dropdown(address_province),
                        "state": dropdown(address_district),
                        "zip_code": customer_address.zip_code
                    }
                })
            domestic_contact_information_detail["resident_address"].update({
                "domestic_flag": customer_address.address_domestic_flag
            })

        if customer_address.address_type_id == CONTACT_ADDRESS_CODE:
            domestic_contact_information_detail["contact_address"] = {
                "country": dropdown(address_country),
                "province": dropdown(address_province),
                "district": dropdown(address_district),
                "ward": dropdown(address_ward),
                "number_and_street": customer_address.address
            }

    _, _, _, _, _, customer_professional, career, average_income_amount, company_position = customer_addresses[0]

    domestic_contact_information_detail["career_information"] = {
        "career": dropdown(career),
        "average_income_amount": dropdown(average_income_amount),
        "company_name": customer_professional.company_name,
        "company_phone": customer_professional.company_phone,
        "company_position": dropdown(company_position),
        "company_address": customer_professional.company_address
    }

    return ReposReturn(data=domestic_contact_information_detail)


@auto_commit
async def repos_save_contact_information(
    cif_id: str,
    customer_professional_id: str,
    is_create: bool,
    is_passport: bool,
    saving_resident_address: dict,
    saving_contact_address: dict,
    saving_career_information: dict,
    log_data: json,
    session: Session
) -> ReposReturn:
    if is_create:
        if is_passport:
            session.add_all([
                CustomerAddress(**saving_resident_address),
                CustomerAddress(**saving_contact_address),
            ])

        session.add(CustomerProfessional(**saving_career_information))
        # Cập nhật lại thông tin nghề nghiệp khách hàng
        session.execute(
            update(Customer).where(Customer.id == cif_id).values(customer_professional_id=customer_professional_id)
        )
    else:
        if is_passport:
            session.execute(
                update(CustomerAddress).where(and_(
                    CustomerAddress.customer_id == cif_id,
                    CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE
                )).values(**saving_resident_address)
            )

            session.execute(
                update(CustomerAddress).where(and_(
                    CustomerAddress.customer_id == cif_id,
                    CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE
                )).values(**saving_contact_address)
            )

        session.execute(
            update(CustomerProfessional).where(and_(
                CustomerProfessional.id == customer_professional_id,
            )).values(**saving_career_information)
        )

        # update booking & log
        fail_result = await write_transaction_log_and_update_booking(
            description="Tạo CIF -> Thông tin cá nhân -> Thông tin liên lạc -- Cập nhật",
            log_data=log_data,
            session=session,
            customer_id=cif_id
        )
        if fail_result:
            return fail_result

    return ReposReturn(data={
        "cif_id": cif_id
    })


########################################################################################################################
# Others
########################################################################################################################
async def repos_get_customer_addresses(cif_id: str, session: Session):
    customer_addresses = session.execute(
        select(CustomerAddress).filter(CustomerAddress.customer_id == cif_id)).scalars().all()
    return ReposReturn(data=customer_addresses)


async def repos_get_customer_professional_and_identity_and_address(cif_id: str, session: Session):
    customer_professional = session.execute(
        select(
            Customer,
            CustomerProfessional,
            CustomerIdentity,
            CustomerAddress
        )
        .join(CustomerProfessional, and_(
            Customer.customer_professional_id == CustomerProfessional.id,
        ))
        .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
        .join(CustomerAddress, Customer.id == CustomerAddress.customer_id)
        .filter(Customer.id == cif_id)
    ).all()
    return ReposReturn(data=customer_professional)
