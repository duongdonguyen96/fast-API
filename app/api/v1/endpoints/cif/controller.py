import re

from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.repository import (
    repos_check_exist_cif, repos_customer_information, repos_get_cif_info,
    repos_profile_history
)
from app.utils.error_messages import ERROR_CIF_NUMBER_INVALID, MESSAGE_STATUS


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
        customer_information = self.call_repos(await repos_customer_information(cif_id))

        return self.response(data=customer_information)

    async def ctr_check_exist_cif(self, cif_number: str):
        regex = re.search("[0-9]+", cif_number)
        if not regex or len(regex.group()) != len(cif_number):
            return self.response_exception(msg=ERROR_CIF_NUMBER_INVALID, detail=MESSAGE_STATUS[ERROR_CIF_NUMBER_INVALID])

        check_exist_info = self.call_repos(
            await repos_check_exist_cif(cif_number=cif_number)
        )
        return self.response(data=check_exist_info)
