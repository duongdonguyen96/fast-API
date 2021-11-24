from sqlalchemy import and_, select
from sqlalchemy.orm import Session

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
from app.utils.functions import datetime_to_date, dropdown, now


async def repos_save_personal(cif_id: str, personal: PersonalRequest, created_by: str, ) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_get_personal_data(cif_id: str, session: Session) -> ReposReturn:

    query_data = session.execute(
        select(
            Customer,
            CustomerIndividualInfo,
            CustomerGender,
            CustomerTitle,
            AddressProvince,
            AddressCountry,
            MaritalStatus,
            ResidentStatus
        ).join(
            Customer, CustomerIndividualInfo.customer_id == Customer.id
        ).join(
            CustomerGender, CustomerIndividualInfo.gender_id == CustomerGender.id
        ).join(
            CustomerTitle, CustomerIndividualInfo.title_id == CustomerTitle.id
        ).join(
            AddressProvince, CustomerIndividualInfo.place_of_birth_id == AddressProvince.id
        ).join(
            AddressCountry, CustomerIndividualInfo.country_of_birth_id == AddressCountry.id
        ).join(
            MaritalStatus, CustomerIndividualInfo.marital_status_id == MaritalStatus.id
        ).join(
            ResidentStatus, CustomerIndividualInfo.resident_status_id == ResidentStatus.id
        ).filter(CustomerIndividualInfo.customer_id == cif_id)
    ).all()

    if not query_data:
        return ReposReturn(is_error=True, msg='cif_id not have customer individual info', loc='cif_id')

    # lấy dữ liệu quốc gia
    query_data_national = session.execute(
        select(
            AddressCountry
        ).join(
            Customer, and_(
                AddressCountry.id == Customer.nationality_id,
                Customer.id == cif_id
            )
        ).filter(AddressCountry.id == Customer.nationality_id)
    ).scalars().first()

    if not query_data_national:
        return ReposReturn(is_error=True, msg='ERROR_NATIONAL_NOT_EXIST', detail='cif_id not national', loc="cif_id")

    # lấy dữ liệu contact_type từ bảng contact_type_dât theo cif_id
    query_data_contact = session.execute(
        select(
            CustomerContactTypeData,
            CustomerContactType
        ).filter(CustomerContactTypeData.customer_id == cif_id)
    ).all()

    if not query_data:
        return ReposReturn(is_error=True, msg='cif_id not have customer individual info', loc='cif_id')

    data_contact = {
        'email_flag': 0,
        'mobile_number_flag': 0
    }
    # TODO: chưa có rule và data contact type nên đang để test
    for customer_contact_type_data, customer_contact_type in query_data_contact:
        if customer_contact_type.name == 'BE_TEST1':
            data_contact['email_flag'] = customer_contact_type_data.active_flag

        if customer_contact_type.name == 'BE_TEST':
            data_contact['mobile_number_flag'] = customer_contact_type_data.active_flag

    data_response = {}
    for customer, customer_individual_info, customer_gender, customer_title, address_province, address_country, \
            marital_status, resident_status in query_data:
        data_response = {
            "full_name_vn": customer.full_name_vn,
            "gender": dropdown(customer_gender),
            "honorific": dropdown(customer_title),
            "date_of_birth": datetime_to_date(customer_individual_info.date_of_birth),
            "under_15_year_old_flag": customer_individual_info.under_15_year_old_flag,
            "place_of_birth": dropdown(address_province),
            "country_of_birth": dropdown(address_country),
            "nationality": dropdown(query_data_national),
            "tax_number": customer.tax_number,
            "resident_status": dropdown(resident_status),
            "mobile_number": customer.mobile_number,
            "telephone_number": customer.telephone_number,
            "email": customer.email,
            "contact_method": data_contact,
            "marital_status": dropdown(marital_status)
        }

    return ReposReturn(data=data_response)
