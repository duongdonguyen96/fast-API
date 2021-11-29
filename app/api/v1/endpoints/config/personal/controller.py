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
                model=CustomerGender
            )
        )
        return self.response(gender_info)

    async def ctr_nationality_info(self):
        nationality_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=AddressCountry
            )
        )
        return self.response(nationality_info)

    async def ctr_ethnic_info(self):
        ethnic_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=Nation
            )
        )
        return self.response(ethnic_info)

    async def ctr_religion_info(self):
        religion_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=Religion
            )
        )
        return self.response(religion_info)

    async def ctr_honorific_info(self):
        honorific_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=CustomerTitle
            )
        )
        return self.response(honorific_info)

    async def ctr_resident_status_info(self):
        resident_status_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=ResidentStatus
            )
        )
        return self.response(resident_status_info)

    async def ctr_marital_status_info(self):
        marital_status_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=MaritalStatus
            )
        )
        return self.response(marital_status_info)

    async def ctr_career_info(self):
        career_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=Career
            )
        )
        return self.response(career_info)

    async def ctr_average_income_amount_info(self):
        average_income_amount_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=AverageIncomeAmount
            )
        )
        return self.response(average_income_amount_info)

    async def ctr_customer_relationship_info(self):
        customer_relationship_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=CustomerRelationshipType
            )
        )
        return self.response(customer_relationship_info)
