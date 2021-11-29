from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.address.repository import (
    repos_get_country, repos_get_district, repos_get_province, repos_get_ward
)


class CtrAddress(BaseController):
    async def ctr_province_info(self, country_id: str):
        provinces_info = self.call_repos(await repos_get_province(country_id=country_id, session=self.oracle_session))
        return self.response(provinces_info)

    async def ctr_district_info(self, province_id: str):
        districts_info = self.call_repos(await repos_get_district(province_id=province_id, session=self.oracle_session))
        return self.response(districts_info)

    async def ctr_ward_info(self, district_id: str):
        wards_info = self.call_repos(await repos_get_ward(district_id=district_id, session=self.oracle_session))
        return self.response(wards_info)

    async def ctr_place_of_issue(self, country_id: str):
        place_of_issues_info = self.call_repos(
            await repos_get_province(country_id=country_id, session=self.oracle_session)
        )
        return self.response(place_of_issues_info)

    async def ctr_country_info(self):
        country_info = self.call_repos(await repos_get_country(self.oracle_session))
        return self.response(country_info)
