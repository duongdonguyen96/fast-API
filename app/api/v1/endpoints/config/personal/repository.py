from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.address import AddressCountry
from app.third_parties.oracle.models.master_data.customer import (
    CustomerGender, CustomerTitle
)
from app.third_parties.oracle.models.master_data.others import Nation, Religion


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
