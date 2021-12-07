from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.payment_account.detail.repository import (
    repos_detail_payment_account, repos_save_payment_account
)
from app.api.v1.endpoints.cif.payment_account.detail.schema import (
    SavePaymentAccountRequest
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.third_parties.oracle.models.master_data.account import (
    AccountClass, AccountType
)
from app.third_parties.oracle.models.master_data.others import Currency
from app.utils.constant.cif import STAFF_TYPE_BUSINESS_CODE
from app.utils.functions import now


class CtrPaymentAccount(BaseController):
    async def detail(self, cif_id: str):
        detail_payment_account_info = self.call_repos(await repos_detail_payment_account(cif_id=cif_id))
        return self.response(data=detail_payment_account_info)

    async def save(self,
                   cif_id,
                   payment_account_save_request: SavePaymentAccountRequest):

        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        # check currency exist
        await self.get_model_object_by_id(
            model=Currency,
            model_id=payment_account_save_request.currency.id,
            loc="currency"
        )

        # check account_type exist
        await self.get_model_object_by_id(
            model=AccountType,
            model_id=payment_account_save_request.account_type.id,
            loc="account type"

        )

        # check account_class exist
        await self.get_model_object_by_id(
            model=AccountClass,
            model_id=payment_account_save_request.account_class.id,
            loc="account class"

        )

        list_data_insert = [{
            "customer_id": cif_id,
            "case_account_number": payment_account_save_request.casa_account_number,
            "currency_id": payment_account_save_request.currency.id,
            'acc_type_id': payment_account_save_request.account_type.id,
            'acc_class_id': payment_account_save_request.account_class.id,
            'acc_structure_type_id': payment_account_save_request.account_structure_type_level_3.id,
            "staff_type_id": STAFF_TYPE_BUSINESS_CODE,
            "acc_salary_org_name": None,
            "acc_salary_org_acc": payment_account_save_request.account_salary_organization_account,
            "maker_id": self.current_user.user_id,
            "maker_at": now(),
            "checker_id": 1,
            "checker_at": None,
            "approve_status": None,
            "self_selected_account_flag": payment_account_save_request.self_selected_account_flag,
            "acc_active_flag": 1,
            "created_at": now(),
            "updated_at": now(),
        }
        ]

        save_payment_account_info = self.call_repos(
            await repos_save_payment_account(
                cif_id=cif_id,
                list_data_insert=list_data_insert,
                created_by=self.current_user.full_name_vn,
                session=self.oracle_session

            ))

        return self.response(data=save_payment_account_info)
