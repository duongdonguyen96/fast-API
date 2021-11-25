from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.personal.repository import (
    repos_get_average_income_amount, repos_get_career,
    repos_get_customer_relationship, repos_get_ethnic, repos_get_gender,
    repos_get_honorific, repos_get_marital_status, repos_get_nationality,
    repos_get_religion, repos_get_resident_status
)


class CtrConfigPersonal(BaseController):
    async def ctr_gender_info(self):
        gender_info = self.call_repos(await repos_get_gender(self.oracle_session))
        return self.response(gender_info)

    async def ctr_nationality_info(self):
        nationality_info = self.call_repos(await repos_get_nationality(self.oracle_session))
        return self.response(nationality_info)

    async def ctr_ethnic_info(self):
        ethnic_info = self.call_repos(await repos_get_ethnic(self.oracle_session))
        return self.response(ethnic_info)

    async def ctr_religion_info(self):
        religion_info = self.call_repos(await repos_get_religion(self.oracle_session))
        return self.response(religion_info)

    async def ctr_honorific_info(self):
        honorific_info = self.call_repos(await repos_get_honorific(self.oracle_session))
        return self.response(honorific_info)

    async def ctr_resident_status_info(self):
        resident_status_info = self.call_repos(await repos_get_resident_status(self.oracle_session))
        return self.response(resident_status_info)

    async def ctr_marital_status_info(self):
        marital_status_info = self.call_repos(await repos_get_marital_status(self.oracle_session))
        return self.response(marital_status_info)

    async def ctr_career_info(self):
        career_info = self.call_repos(await repos_get_career(self.oracle_session))
        return self.response(career_info)

    async def ctr_average_income_amount_info(self):
        average_income_amount_info = self.call_repos(await repos_get_average_income_amount(self.oracle_session))
        return self.response(average_income_amount_info)

    async def ctr_customer_relationship_info(self):
        customer_relationship_info = self.call_repos(await repos_get_customer_relationship(self.oracle_session))
        return self.response(customer_relationship_info)
