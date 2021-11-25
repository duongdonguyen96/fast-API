from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.personal.repository import (
    repos_get_contact_type, repos_get_contact_type_data,
    repos_get_personal_data, repos_save_personal
)
from app.api.v1.endpoints.cif.basic_information.personal.schema import (
    PersonalRequest
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.utils.functions import now


class CtrPersonal(BaseController):
    async def ctr_save_personal(self, cif_id: str, personal: PersonalRequest):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))
        # lấy data từ contact_type
        contact_type = self.call_repos(await repos_get_contact_type(session=self.oracle_session))

        contact_type_data = self.call_repos(
            await repos_get_contact_type_data(cif_id=cif_id, session=self.oracle_session))

        # taọ data contact_type_data insert and update
        list_contact_type_data = []
        # TODO : chưa có data contact_type nên đang để test
        for item in contact_type:
            default_data = {
                "customer_contact_type_id": item.id,
                "customer_id": cif_id,
                "customer_contact_type_created_at": now(),
            }
            if item.name == 'BE_TEST1':
                default_data.update({
                    "active_flag": personal.contact_method.email_flag
                })

            if item.name == 'BE_TEST':
                default_data.update({
                    "active_flag": personal.contact_method.mobile_number_flag
                })
            list_contact_type_data.append(default_data)

        personal_data = self.call_repos(
            await repos_save_personal(
                cif_id=cif_id,
                personal=personal,
                contact_type_data=contact_type_data,
                list_contact_type_data=list_contact_type_data,
                session=self.oracle_session,
                created_by=self.current_user.full_name_vn
            )
        )

        return self.response(data=personal_data)

    async def ctr_personal(self, cif_id: str):
        personal_data = self.call_repos(await repos_get_personal_data(cif_id))

        return self.response(data=personal_data)
