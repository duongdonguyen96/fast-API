from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.payment_account.co_owner.repository import (
    repos_check_list_cif_number, repos_detail_co_owner, repos_get_casa_account,
    repos_get_co_owner_data, repos_save_co_owner
)
from app.api.v1.endpoints.cif.payment_account.co_owner.schema import (
    AccountHolderRequest
)
from app.utils.functions import generate_uuid


class CtrCoOwner(BaseController):
    async def ctr_save_co_owner(self, cif_id: str, co_owner: AccountHolderRequest):
        # lấy casa_account_id theo số cif_id
        casa_account = self.call_repos(await repos_get_casa_account(cif_id=cif_id, session=self.oracle_session))

        # lấy danh sách cif_number account request
        list_cif_number_request = []
        for cif_number in co_owner.joint_account_holders:
            list_cif_number_request.append(cif_number.cif_number)

        # check cif_number có tồn tại
        self.call_repos(
            await repos_check_list_cif_number(
                list_cif_number_request=list_cif_number_request,
                session=self.oracle_session
            )
        )
        save_account_holder = [{
            "id": generate_uuid(),
            "cif_num": cif_number.cif_number,
            "casa_account_id": casa_account,
            "joint_account_holder_flag": co_owner.joint_account_holder_flag,
            "joint_account_holder_no": 1
        } for cif_number in co_owner.joint_account_holders]

        save_account_agree = []
        for agreement in co_owner.agreement_authorization:
            for signature in agreement.signature_list:
                for account_holder in save_account_holder:
                    if signature.cif_number == account_holder['cif_num']:
                        save_account_agree.append({
                            "agreement_authorization_id": agreement.id,
                            "joint_account_holder_id": account_holder['id'],
                            "agreement_flag": agreement.agreement_flag,
                            "method_sign": agreement.method_sign
                        })

        co_owner_data = self.call_repos(
            await repos_save_co_owner(
                cif_id=cif_id,
                save_account_holder=save_account_holder,
                save_account_agree=save_account_agree,
                session=self.oracle_session,
                created_by=self.current_user.full_name_vn,
            )
        )

        return self.response(data=co_owner_data)

    async def ctr_co_owner(self, cif_id: str):
        co_owner_data = self.call_repos(await repos_get_co_owner_data(cif_id=cif_id, session=self.oracle_session))

        return self.response(data=co_owner_data)

    async def detail_co_owner(self, cif_id: str, cif_number_need_to_find: str):
        detail_co_owner = self.call_repos(await repos_detail_co_owner(
            cif_id=cif_id,
            cif_number_need_to_find=cif_number_need_to_find,
            session=self.oracle_session
        ))

        return self.response(data=detail_co_owner)
