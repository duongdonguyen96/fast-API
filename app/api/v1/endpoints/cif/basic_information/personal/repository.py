from typing import List

from sqlalchemy import select, update
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
from app.third_parties.oracle.models.master_data.customer import (
    CustomerContactType
)
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import now


async def repos_get_contact_type_data(cif_id: str, session: Session):
    contact_type_data = session.execute(
        select(
            CustomerContactTypeData
        ).filter(CustomerContactTypeData.customer_id == cif_id)
    ).scalars().all()

    return ReposReturn(data=contact_type_data)


async def repos_get_contact_type(session: Session):
    contact_type = session.execute(
        select(CustomerContactType)
    ).scalars().all()
    return ReposReturn(data=contact_type)


async def repos_save_personal(
        cif_id: str,
        personal: PersonalRequest,
        contact_type_data: List,
        list_contact_type_data: List,
        session: Session,
        created_by: str
) -> ReposReturn:
    session.execute(
        update(
            Customer
        ).where(Customer.id == cif_id).values(
            # TODO: fullname, lastname, ...
            full_name_vn=personal.full_name_vn,
            email=personal.email,
            telephone_number=personal.telephone_number,
            mobile_number=personal.mobile_number,
            tax_number=personal.tax_number,
            nationality_id=personal.nationality.id
        )
    )
    session.execute(
        update(
            CustomerIndividualInfo
        ).where(CustomerIndividualInfo.customer_id == cif_id).values(
            gender_id=personal.gender.id,
            title_id=personal.honorific.id,
            date_of_birth=personal.date_of_birth,
            place_of_birth_id=personal.place_of_birth.id,
            country_of_birth_id=personal.country_of_birth.id,
            resident_status_id=personal.resident_status.id,
            marital_status_id=personal.marital_status.id
        )
    )
    # check contact_type_data
    if not contact_type_data:
        data_insert_contact_type = [CustomerContactTypeData(**data_insert) for data_insert in list_contact_type_data]
        session.bulk_save_objects(data_insert_contact_type)
    else:
        session.bulk_update_mappings(CustomerContactTypeData, list_contact_type_data)

    session.commit()
    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_get_personal_data(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={

        "full_name_vn": "TRẦN MINH HUYỀN",
        "gender": {
            "id": "1",
            "name": "Nữ",
            "code": "Code"
        },
        "honorific": {
            "id": "1",
            "name": "Chị",
            "code": "Code"
        },
        "date_of_birth": "1995-03-20",
        "under_15_year_old_flag": False,
        "place_of_birth": {
            "id": "1",
            "name": "Hồ Chí Minh",
            "code": "Code"
        },
        "country_of_birth": {
            "id": "1",
            "name": "Việt Nam",
            "code": "Code"
        },
        "nationality": {
            "id": "1",
            "name": "Việt Nam",
            "code": "Code"
        },
        "tax_number": "DN251244124",
        "resident_status": {
            "id": "1",
            "name": "Cư trú",
            "code": "Code"
        },
        "mobile_number": "21352413652",
        "telephone_number": "0235641145",
        "email": "tranminhhuyen@gmail.com",
        "contact_method": {
            "email_flag": True,
            "mobile_number_flag": True
        },
        "marital_status": {
            "id": "1",
            "name": "Độc thân",
            "code": "12345"
        }
    })
