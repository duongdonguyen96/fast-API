from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.address import AddressCountry
from app.third_parties.oracle.models.master_data.customer import (
    CustomerGender, CustomerRelationshipType, CustomerTitle
)
from app.third_parties.oracle.models.master_data.others import (
    AverageIncomeAmount, Career, MaritalStatus, Nation, Religion,
    ResidentStatus
)


class CtrConfigPersonal(BaseController):
    async def ctr_gender_info(self):
        gender_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=CustomerGender,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(gender_info)

    async def ctr_nationality_info(self):
        nationality_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=AddressCountry,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(nationality_info)

    async def ctr_ethnic_info(self):
        ethnic_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=Nation,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(ethnic_info)

    async def ctr_religion_info(self):
        religion_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=Religion,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(religion_info)

    async def ctr_honorific_info(self):
        honorific_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=CustomerTitle,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(honorific_info)

    async def ctr_resident_status_info(self):
        resident_status_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=ResidentStatus,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(resident_status_info)

    async def ctr_marital_status_info(self):
        marital_status_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=MaritalStatus,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(marital_status_info)

    async def ctr_career_info(self):
        career_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=Career,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(career_info)

    async def ctr_average_income_amount_info(self):
        average_income_amount_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=AverageIncomeAmount,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(average_income_amount_info)

    async def ctr_customer_relationship_info(self):
        customer_relationship_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=CustomerRelationshipType,
                country_id=None,
                province_id=None,
                district_id=None
            )
        )
        return self.response(customer_relationship_info)
