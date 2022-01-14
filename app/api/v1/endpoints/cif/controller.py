from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.repository import (
    repos_customer_information, repos_get_cif_info, repos_profile_history
)
from app.utils.functions import dropdown, dropdownflag


class CtrCustomer(BaseController):
    async def ctr_cif_info(self, cif_id: str):
        cif_info = self.call_repos(
            await repos_get_cif_info(
                cif_id=cif_id,
                session=self.oracle_session
            ))
        return self.response(cif_info)

    async def ctr_profile_history(self, cif_id: str):
        profile_history = self.call_repos((await repos_profile_history(cif_id)))
        return self.response(profile_history)

    async def ctr_customer_information(self, cif_id: str):
        customer_information = self.call_repos(
            await repos_customer_information(cif_id=cif_id, session=self.oracle_session))
        first_row = customer_information[0]

        data_response = {
            "customer_id": first_row.Customer.id,
            "status": dropdownflag(first_row.CustomerStatus),
            "cif_number": first_row.Customer.cif_number,
            "avatar_url": first_row.Customer.avatar_url,
            "customer_classification": dropdown(first_row.CustomerClassification),
            "full_name": first_row.Customer.full_name,
            "gender": dropdown(first_row.CustomerGender),
            "email": first_row.Customer.email,
            "mobile_number": first_row.Customer.mobile_number,
            "identity_number": first_row.CustomerIdentity.identity_num,
            "place_of_issue": dropdown(first_row.PlaceOfIssue),
            "issued_date": first_row.CustomerIdentity.issued_date,
            "expired_date": first_row.CustomerIdentity.expired_date,
            "date_of_birth": first_row.CustomerIndividualInfo.date_of_birth,
            "nationality": dropdown(first_row.AddressCountry),
            "marital_status": dropdown(first_row.MaritalStatus),
            "customer_type": dropdown(first_row.CustomerType),
            "credit_rating": None,
            "address": first_row.CustomerAddress.address
        }

        return self.response(data=data_response)
