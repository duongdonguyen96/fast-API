from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)


async def repos_get_province(country_id: str, session: Session) -> ReposReturn:

    provinces = session.execute(
        select(
            AddressProvince
        ).filter(
            AddressProvince.country_id == country_id
        )
    ).scalars().all()
    if not provinces:
        return ReposReturn(is_error=True, msg="province doesn't have data", loc='config')
    list_return_province_config = []
    for province in provinces:
        list_return_province_config.append({
            "id": province.id,
            "code": province.code,
            "name": province.name
        })

    return ReposReturn(data=list_return_province_config)


async def repos_get_district(province_id: str, session: Session) -> ReposReturn:

    districts = session.execute(
        select(
            AddressDistrict
        ).filter(AddressDistrict.province_id == province_id)
    ).scalars().all()
    if not districts:
        return ReposReturn(is_error=True, msg="district doesn't have data", loc='config')
    list_return_province_config = []
    for district in districts:
        list_return_province_config.append({
            "id": district.id,
            "code": district.code,
            "name": district.name
        })

    return ReposReturn(data=list_return_province_config)


async def repos_get_ward(district_id: str, session: Session) -> ReposReturn:

    wards = session.execute(
        select(
            AddressWard
        ).filter(AddressWard.district_id == district_id)
    ).scalars().all()
    if not wards:
        return ReposReturn(is_error=True, msg="ward doesn't have data", loc='config')
    list_return_ward_config = []
    for ward in wards:
        list_return_ward_config.append({
            "id": ward.id,
            "code": ward.code,
            "name": ward.name
        })

    return ReposReturn(data=list_return_ward_config)


async def repos_get_place_of_issue(country_id: str, session: Session) -> ReposReturn:

    place_of_issues = session.execute(
        select(
            AddressProvince
        ).filter(
            AddressProvince.country_id == country_id
        )
    ).scalars().all()
    if not place_of_issues:
        return ReposReturn(is_error=True, msg="place_of_issue doesn't have data", loc='config')
    list_return_province_config = []
    for place_of_issue in place_of_issues:
        list_return_province_config.append({
            "id": place_of_issue.id,
            "code": place_of_issue.code,
            "name": place_of_issue.name
        })

    return ReposReturn(data=list_return_province_config)


async def repos_get_country(session: Session) -> ReposReturn:

    countries = session.execute(select(AddressCountry)).scalars().all()
    if not countries:
        return ReposReturn(is_error=True, msg="country doesn't have data", loc='config')
    list_country_config = []
    for country in countries:
        list_country_config.append({
            "id": country.id,
            "code": country.code,
            "name": country.name
        })

    return ReposReturn(data=list_country_config)
