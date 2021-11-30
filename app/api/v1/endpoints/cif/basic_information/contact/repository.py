from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.contact.model import (
    CustomerAddress, CustomerProfessional
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
from app.utils.constant.cif import (
    CIF_ID_TEST, CONTACT_ADDRESS_CODE, RESIDENT_ADDRESS_CODE
)
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import dropdown, now


async def repos_get_detail_contact_information(cif_id: str, session: Session) -> ReposReturn:
    domestic_contact_information_detail = {
        "resident_address": {}
    }
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

    for customer_address, address_country, address_province, address_district, address_ward, _, _, _, _ in customer_addresses:
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
                    "foreign_address": {
                        "country": {
                            "id": None,
                            "code": None,
                            "name": None
                        },
                        "address_1": None,
                        "address_2": None,
                        "province": {
                            "id": None,
                            "code": None,
                            "name": None
                        },
                        "state": {
                            "id": None,
                            "code": None,
                            "name": None
                        },
                        "zip_code": None
                    }
                })
            else:
                print(address_country)
                domestic_contact_information_detail["resident_address"].update({
                    "foreign_address": {
                        "country": dropdown(address_country),
                        "address_1": customer_address.address,
                        "address_2": customer_address.address_2,
                        "province": dropdown(address_province),
                        "state": dropdown(address_district),
                        "zip_code": customer_address.zip_code
                    },
                    "domestic_address": {
                        "country": {
                            "id": None,
                            "code": None,
                            "name": None
                        },
                        "number_and_street": None,
                        "province": {
                            "id": None,
                            "code": None,
                            "name": None
                        },
                        "district": {
                            "id": None,
                            "code": None,
                            "name": None
                        },
                        "ward": {
                            "id": None,
                            "code": None,
                            "name": None
                        }
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


async def repos_save_contact_information(
        cif_id: str,
        created_by
) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })
