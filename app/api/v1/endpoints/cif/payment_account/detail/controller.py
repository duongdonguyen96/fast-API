from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.payment_account.detail.repository import (
    repos_check_casa_account, repos_detail_payment_account,
    repos_save_payment_account
)
from app.api.v1.endpoints.cif.payment_account.detail.schema import (
    SavePaymentAccountRequest
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.api.v1.endpoints.repository import repos_get_acc_structure_type
from app.third_parties.oracle.models.master_data.account import (
    AccountClass, AccountType
)
from app.third_parties.oracle.models.master_data.others import Currency
from app.utils.constant.cif import (
    ACC_STRUCTURE_TYPE_LEVEL_3, STAFF_TYPE_BUSINESS_CODE
)
from app.utils.error_messages import ERROR_NOT_NULL, MESSAGE_STATUS
from app.utils.functions import now


class CtrPaymentAccount(BaseController):

    async def detail(self, cif_id: str):
        detail_payment_account_info = self.call_repos(
            await repos_detail_payment_account(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )

        return self.response(detail_payment_account_info)

    async def save(self,
                   cif_id: str,
                   payment_account_save_request: SavePaymentAccountRequest):

        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        # check TKTT đã tạo hay chưa
        is_created = True
        # Không cần gọi self.call_repos
        casa_account = await repos_check_casa_account(
            cif_id=cif_id,
            session=self.oracle_session
        )
        if casa_account.data:
            is_created = False

        # Nếu là Tài khoản yêu cầu
        self_selected_account_flag = payment_account_save_request.self_selected_account_flag
        if self_selected_account_flag:
            # TODO: Số tài khoản có thể có yêu cầu nghiệp vụ về độ dài tùy theo kiểu kiến trúc, VALIDATE
            if not payment_account_save_request.casa_account_number:
                return self.response_exception(
                    msg=f"casa_account_number {MESSAGE_STATUS[ERROR_NOT_NULL]}",
                    loc="casa_account_number"
                )

            # check acc_structure_type_level_3_id required
            if not payment_account_save_request.account_structure_type_level_3.id:
                return self.response_exception(
                    msg=f"ID {MESSAGE_STATUS[ERROR_NOT_NULL]}",
                    loc="account_structure_type_level_3 -> id"
                )

            # check acc_structure_type_level_3_id exist
            # Trường hợp đặc biệt, phải check luôn cả loại kiến trúc là cấp 3 nên không dùng get_model_object_by_id
            self.call_repos(
                await repos_get_acc_structure_type(
                    acc_structure_type_id=payment_account_save_request.account_structure_type_level_3.id,
                    level=ACC_STRUCTURE_TYPE_LEVEL_3,
                    loc="account_structure_type_level_3",
                    session=self.oracle_session
                )
            )

        # TODO: Tài khoản của tổ chức chi lương chưa được mô tả
        # TODO: Tên tài khoản của tổ chức chi lương chưa được mô tả
        # TODO: Mở tài khoản thông thường, hiện tại không gửi data để lưu kiểu kiến trúc cấp 3

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
            loc="account_type"
        )

        # check account_class exist
        await self.get_model_object_by_id(
            model=AccountClass,
            model_id=payment_account_save_request.account_class.id,
            loc="account_class"
        )

        data_insert = {
            "customer_id": cif_id,
            "casa_account_number": payment_account_save_request.casa_account_number,
            "currency_id": payment_account_save_request.currency.id,
            'acc_type_id': payment_account_save_request.account_type.id,
            'acc_class_id': payment_account_save_request.account_class.id,
            'acc_structure_type_id': payment_account_save_request.account_structure_type_level_3.id,
            "staff_type_id": STAFF_TYPE_BUSINESS_CODE,
            "acc_salary_org_name": payment_account_save_request.account_salary_organization_name,
            "acc_salary_org_acc": payment_account_save_request.account_salary_organization_account,
            "maker_id": self.current_user.user_id,
            "maker_at": now(),
            "checker_id": 1,
            "checker_at": None,
            "approve_status": None,
            "self_selected_account_flag": self_selected_account_flag,
            "acc_active_flag": 1,
            "created_at": now(),
            "updated_at": now(),
        }

        save_payment_account_info = self.call_repos(
            await repos_save_payment_account(
                cif_id=cif_id,
                data_insert=data_insert,
                log_data=payment_account_save_request.json(),
                created_by=self.current_user.full_name_vn,
                session=self.oracle_session,
                is_created=is_created
            ))

        return self.response(data=save_payment_account_info)
