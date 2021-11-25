from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.address import AddressCountry
from app.third_parties.oracle.models.master_data.customer import (
    CustomerGender, CustomerRelationshipType, CustomerTitle
)
from app.third_parties.oracle.models.master_data.others import (
    AverageIncomeAmount, Career, MaritalStatus, Nation, Religion,
    ResidentStatus
)


async def repos_get_gender(session: Session) -> ReposReturn:

    genders = session.execute(select(CustomerGender)).scalars().all()
    if not genders:
        return ReposReturn(is_error=True, msg="gender doesn't have data", loc='config')
    list_gender_config = []
    for gender in genders:
        list_gender_config.append({
            "id": gender.id,
            "code": gender.code,
            "name": gender.name
        })

    return ReposReturn(data=list_gender_config)


async def repos_get_nationality(session: Session) -> ReposReturn:

    nationalities = session.execute(select(AddressCountry)).scalars().all()
    if not nationalities:
        return ReposReturn(is_error=True, msg="nationality doesn't have data", loc='config')
    list_nationality_config = []
    for nationality in nationalities:
        list_nationality_config.append({
            "id": nationality.id,
            "code": nationality.code,
            "name": nationality.name
        })

    return ReposReturn(data=list_nationality_config)


async def repos_get_ethnic(session: Session) -> ReposReturn:

    ethnics = session.execute(select(Nation)).scalars().all()
    if not ethnics:
        return ReposReturn(is_error=True, msg="ethnic doesn't have data", loc='config')
    list_ethnic_config = []
    for ethnic in ethnics:
        list_ethnic_config.append({
            "id": ethnic.id,
            "code": ethnic.code,
            "name": ethnic.name
        })

    return ReposReturn(data=list_ethnic_config)


async def repos_get_religion(session: Session) -> ReposReturn:

    religions = session.execute(select(Religion)).scalars().all()
    if not religions:
        return ReposReturn(is_error=True, msg="religion doesn't have data", loc='config')
    list_religion_config = []
    for religion in religions:
        list_religion_config.append({
            "id": religion.id,
            "code": religion.code,
            "name": religion.name
        })

    return ReposReturn(data=list_religion_config)


async def repos_get_honorific(session: Session) -> ReposReturn:

    honorifics = session.execute(select(CustomerTitle)).scalars().all()
    if not honorifics:
        return ReposReturn(is_error=True, msg="honorific doesn't have data", loc='config')
    list_honorific_config = []
    for honorific in honorifics:
        list_honorific_config.append({
            "id": honorific.id,
            "code": honorific.code,
            "name": honorific.name
        })

    return ReposReturn(data=list_honorific_config)


async def repos_get_resident_status(session: Session) -> ReposReturn:

    list_resident_status = session.execute(select(ResidentStatus)).scalars().all()
    if not list_resident_status:
        return ReposReturn(is_error=True, msg="resident_status doesn't have data", loc='config')
    list_resident_status_config = []
    for resident_status in list_resident_status:
        list_resident_status_config.append({
            "id": resident_status.id,
            "code": resident_status.code,
            "name": resident_status.name
        })

    return ReposReturn(data=list_resident_status_config)


async def repos_get_marital_status(session: Session) -> ReposReturn:

    list_marital_status = session.execute(select(MaritalStatus)).scalars().all()
    if not list_marital_status:
        return ReposReturn(is_error=True, msg="marital_status doesn't have data", loc='config')
    list_marital_status_config = []
    for resident_status in list_marital_status:
        list_marital_status_config.append({
            "id": resident_status.id,
            "code": resident_status.code,
            "name": resident_status.name
        })

    return ReposReturn(data=list_marital_status_config)


async def repos_get_career(session: Session) -> ReposReturn:

    careers = session.execute(select(Career)).scalars().all()
    if not careers:
        return ReposReturn(is_error=True, msg="career doesn't have data", loc='config')
    list_career_config = []
    for career in careers:
        list_career_config.append({
            "id": career.id,
            "code": career.code,
            "name": career.name
        })

    return ReposReturn(data=list_career_config)


async def repos_get_average_income_amount(session: Session) -> ReposReturn:

    average_income_amounts = session.execute(select(AverageIncomeAmount)).scalars().all()
    if not average_income_amounts:
        return ReposReturn(is_error=True, msg="average_income_amount doesn't have data", loc='config')
    list_average_income_amount_config = []
    for average_income_amount in average_income_amounts:
        list_average_income_amount_config.append({
            "id": average_income_amount.id,
            "code": average_income_amount.code,
            "name": average_income_amount.name
        })

    return ReposReturn(data=list_average_income_amount_config)


async def repos_get_customer_relationship(session: Session) -> ReposReturn:

    customer_relationships = session.execute(select(CustomerRelationshipType)).scalars().all()
    if not customer_relationships:
        return ReposReturn(is_error=True, msg="customer_relationship doesn't have data", loc='config')
    list_customer_relationship_config = []
    for customer_relationship in customer_relationships:
        list_customer_relationship_config.append({
            "id": customer_relationship.id,
            "code": customer_relationship.code,
            "name": customer_relationship.name
        })

    return ReposReturn(data=list_customer_relationship_config)
