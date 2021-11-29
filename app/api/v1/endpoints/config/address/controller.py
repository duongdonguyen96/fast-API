from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)


class CtrAddress(BaseController):
    async def ctr_province_info(self, country_id: str):
        provinces_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=AddressProvince,
                country_id=country_id,
                province_id=None,
                district_id=None
            )
        )
        return self.response(provinces_info)

    async def ctr_district_info(self, province_id: str):
        districts_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=AddressDistrict,
                country_id=None,
                province_id=province_id,
                district_id=None
            )
        )
        return self.response(districts_info)

    async def ctr_ward_info(self, district_id: str):
        wards_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=AddressWard,
                country_id=None,
                province_id=None,
                district_id=district_id
            )
        )
        return self.response(wards_info)

    async def ctr_place_of_issue(self, country_id: str):
        place_of_issues_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=AddressProvince,
                country_id=country_id,
                province_id=None,
                district_id=None
            )
        )
        return self.response(place_of_issues_info)

    async def ctr_country_info(self):
        country_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=AddressCountry,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(country_info)
