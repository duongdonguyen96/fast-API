from sqlalchemy import select
from sqlalchemy.orm import Session, aliased

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.cif.basic_information.personal.schema import (
    PersonalRequest
)
from app.third_parties.oracle.models.cif.basic_information.contact.model import (
    CustomerContactTypeData
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.basic_information.personal.model import (
    CustomerIndividualInfo
)
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressProvince
)
from app.third_parties.oracle.models.master_data.customer import (
    CustomerContactType, CustomerGender, CustomerTitle
)
from app.third_parties.oracle.models.master_data.others import (
    MaritalStatus, ResidentStatus
)
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import dropdown, now


async def repos_save_personal(cif_id: str, personal: PersonalRequest, created_by: str, ) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_get_personal_data(cif_id: str, session: Session) -> ReposReturn:
    country = aliased(AddressCountry, name='Country')

    query_data = session.execute(
        select(
            Customer,
            CustomerIndividualInfo,
            CustomerGender,
            CustomerTitle,
            AddressProvince,
            country,
            AddressCountry,
            MaritalStatus,
            ResidentStatus,
            CustomerContactTypeData,
            CustomerContactType
        )
        .join(Customer, CustomerIndividualInfo.customer_id == Customer.id)
        .join(CustomerGender, CustomerIndividualInfo.gender_id == CustomerGender.id)
        .join(CustomerTitle, CustomerIndividualInfo.title_id == CustomerTitle.id)
        .join(AddressProvince, CustomerIndividualInfo.place_of_birth_id == AddressProvince.id)
        .join(country, CustomerIndividualInfo.country_of_birth_id == country.id)
        .join(AddressCountry, Customer.nationality_id == AddressCountry.id)
        .join(MaritalStatus, CustomerIndividualInfo.marital_status_id == MaritalStatus.id)
        .join(ResidentStatus, CustomerIndividualInfo.resident_status_id == ResidentStatus.id)
        .join(CustomerContactTypeData, Customer.id == CustomerContactTypeData.customer_id)
        .join(CustomerContactType, CustomerContactType.id == CustomerContactTypeData.customer_contact_type_id)
        .filter(Customer.id == cif_id)
    ).all()

    if not query_data:
        return ReposReturn(is_error=True, msg='cif_id not have customer individual info', loc='cif_id')

    first_row = query_data[0]
    data_contact = {
        'email_flag': 0,
        'mobile_number_flag': 0
    }

    # TODO: chưa có rule và data contact type nên đang để test
    for row in query_data:
        if row.CustomerContactType.name == 'BE_TEST1':
            data_contact['email_flag'] = row.CustomerContactTypeData.active_flag
        if row.CustomerContactType.name == 'BE_TEST':
            data_contact['mobile_number_flag'] = row.CustomerContactTypeData.active_flag

    data_response = {
        "full_name_vn": first_row.Customer.full_name_vn,
        "gender": dropdown(first_row.CustomerGender),
        "honorific": dropdown(first_row.CustomerTitle),
        "date_of_birth": first_row.CustomerIndividualInfo.date_of_birth,
        "under_15_year_old_flag": first_row.CustomerIndividualInfo.under_15_year_old_flag,
        "place_of_birth": dropdown(first_row.AddressProvince),
        "country_of_birth": dropdown(first_row.Country),
        "nationality": dropdown(first_row.AddressCountry),
        "tax_number": first_row.Customer.tax_number,
        "resident_status": dropdown(first_row.ResidentStatus),
        "mobile_number": first_row.Customer.mobile_number,
        "telephone_number": first_row.Customer.telephone_number,
        "email": first_row.Customer.email,
        "contact_method": data_contact,
        "marital_status": dropdown(first_row.MaritalStatus)
    }

    return ReposReturn(data=data_response)
