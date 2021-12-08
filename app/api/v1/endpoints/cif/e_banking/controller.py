from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.e_banking.repository import (
    repos_balance_saving_account_data, repos_get_detail_reset_password,
    repos_get_detail_reset_password_teller, repos_get_e_banking_data,
    repos_get_list_balance_payment_account, repos_save_e_banking_data
)
from app.api.v1.endpoints.cif.e_banking.schema import EBankingRequest
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.third_parties.oracle.models.cif.e_banking.model import (
    EBankingInfo, EBankingInfoAuthentication,
    EBankingReceiverNotificationRelationship, EBankingRegisterBalance,
    EBankingRegisterBalanceFd, EBankingRegisterBalanceNotification,
    EBankingRegisterBalanceOption
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.customer import (
    CustomerContactType, CustomerRelationshipType
)
from app.third_parties.oracle.models.master_data.e_banking import (
    EBankingNotification
)
from app.third_parties.oracle.models.master_data.others import (
    MethodAuthentication
)
from app.utils.constant.cif import (
    EBANKING_ACCOUNT_TYPE_CHECKING, EBANKING_ACTIVE_PASSWORD_EMAIL,
    EBANKING_ACTIVE_PASSWORD_SMS, EBANKING_HAS_FEE, EBANKING_HAS_NO_FEE
)
from app.utils.functions import generate_uuid


class CtrEBanking(BaseController):
    async def ctr_save_e_banking(self, cif_id: str, e_banking: EBankingRequest):
        current_customer = self.call_repos(
            await repos_get_initializing_customer(
                cif_id=cif_id,
                session=self.oracle_session
            ))
        insert_data = []

        change_of_balance_payment_account = e_banking.change_of_balance_payment_account
        if e_banking.change_of_balance_payment_account.register_flag:
            # lọc và kiểm tra và lấy hình thức liên lạc được đánh dấu có tồn tại hay không ?
            contact_types = await self.get_model_objects_by_ids(
                model=CustomerContactType,
                model_ids=[contact_type.id for contact_type in change_of_balance_payment_account.customer_contact_types
                           if contact_type.checked_flag],
                loc="change_of_balance_payment_account -> customer_contact_types"
            )

            register_balance_casas = change_of_balance_payment_account.register_balance_casas

            # kiểm tra tùy chọn thông báo / loại quan hệ / tài khoản ở mục I có tồn tại hay không ?
            notification_ids, relationship_ids, casa_account_ids = set(), set(), []
            for register_balance_casa in register_balance_casas:
                for notification in register_balance_casa.e_banking_notifications:
                    notification_ids.add(notification.id)
                for relationship in register_balance_casa.notification_casa_relationships:
                    relationship_ids.add(relationship.relationship_type.id)
                casa_account_ids.append(register_balance_casa.account_id)
            # kiểm tra tùy chọn thông báo ở mục I có tồn tại hay không ?
            await self.get_model_objects_by_ids(
                model=EBankingNotification,
                model_ids=list(notification_ids),
                loc="change_of_balance_payment_account -> register_balance_casas -> e_banking_notifications"
            )
            # kiểm tra loại quan hệ ở mục I có tồn tại hay không ?
            await self.get_model_objects_by_ids(
                model=CustomerRelationshipType,
                model_ids=list(relationship_ids),
                loc="notification_casa_relationships -> relationship_type -> id"
            )
            # kiểm tra tài khoản ở mục I có tồn tại hay không ?
            await self.get_model_objects_by_ids(
                model=CasaAccount,
                model_ids=casa_account_ids,
                loc="register_balance_casas -> account_id"
            )

            # lưu hình thức nhận thông báo taì khoản thanh toàn (TKTT) I -> 1
            insert_data.extend([EBankingRegisterBalanceOption(
                customer_id=cif_id,
                e_banking_register_account_type=EBANKING_ACCOUNT_TYPE_CHECKING,
                customer_contact_type_id=contact_type.id
            ) for contact_type in contact_types])

            for register_balance_casa in register_balance_casas:
                # lưu I -> 2 -> b (primary) Thông tin người nhận thông báo
                eb_reg_balance_id = generate_uuid()
                insert_data.append(
                    EBankingRegisterBalance(
                        id=eb_reg_balance_id,
                        customer_id=cif_id,
                        e_banking_register_account_type=EBANKING_ACCOUNT_TYPE_CHECKING,
                        full_name=current_customer.full_name_vn,
                        mobile_number=register_balance_casa.primary_phone_number,
                        account_id=register_balance_casa.account_id,
                        name=register_balance_casa.account_name,
                    ))

                # lưu I -> 2 -> b (relationship) Thông tin người nhận thông báo
                insert_data.extend([
                    EBankingReceiverNotificationRelationship(
                        e_banking_register_balance_casa_id=eb_reg_balance_id,
                        relationship_type_id=relationship.relationship_type.id,
                        mobile_number=relationship.mobile_number,
                        full_name=relationship.full_name_vn
                    ) for relationship in register_balance_casa.notification_casa_relationships
                ])

                # lưu I -> 2 -> c Tùy chọn thông báo
                insert_data.extend([
                    EBankingRegisterBalanceNotification(
                        customer_id=cif_id,
                        e_banking_register_account_type=EBANKING_ACCOUNT_TYPE_CHECKING,
                        eb_notify_id=notification.id,
                    ) for notification in register_balance_casa.e_banking_notifications if notification.checked_flag
                ])

        # Thêm dữ liệu cho mục II. Thông tin biến động tài khoản tiết kiệm
        change_of_balance_saving_account = e_banking.change_of_balance_saving_account
        if change_of_balance_saving_account.register_flag:
            contact_types = await self.get_model_objects_by_ids(
                model=CustomerContactType,
                model_ids=[contact_type.id for contact_type in change_of_balance_payment_account.customer_contact_types
                           if contact_type.checked_flag],
                loc="change_of_balance_saving_account -> customer_contact_types"
            )

            insert_data.extend([EBankingRegisterBalanceOption(
                customer_id=cif_id,
                e_banking_register_account_type=EBANKING_ACCOUNT_TYPE_CHECKING,
                customer_contact_type_id=contact_type.id
            ) for contact_type in contact_types])

            insert_data.extend([EBankingRegisterBalanceFd(
                td_account_id=td_account.id,
                customer_id=cif_id,
            ) for td_account in change_of_balance_saving_account.range.td_accounts if td_account.checked_flag])

            # kiểm tra tùy chọn thông báo ở mục II có tồn tại hay không ?
            await self.get_model_objects_by_ids(
                model=EBankingNotification,
                model_ids=list({
                    notification.id for notification in change_of_balance_saving_account.e_banking_notifications
                    if notification.checked_flag
                }),
                loc="change_of_balance_saving_account -> e_banking_notifications"
            )

            # lưu II -> 4 Tùy chọn thông báo
            insert_data.extend([EBankingRegisterBalanceNotification(
                customer_id=cif_id,
                e_banking_register_account_type=EBANKING_ACCOUNT_TYPE_CHECKING,
                eb_notify_id=notification.id,
            ) for notification in change_of_balance_saving_account.e_banking_notifications if
                notification.checked_flag])

        # Thêm dữ liệu cho mục III. Thông tin e-banking
        # Thông tin tài khoản
        account_information = e_banking.e_banking_information.account_information
        # Tùy chọn tài khoản
        optional_e_banking_account = e_banking.e_banking_information.optional_e_banking_account
        has_fee = None
        if account_information.register_flag:
            # kiểm tra hình thức xác thực có tồn tại hay không ?
            auth_method_ids = [method.id for method in account_information.method_authentication if method.checked_flag]
            auth_types = await self.get_model_objects_by_ids(
                model=MethodAuthentication,
                model_ids=auth_method_ids,
                loc="method_authentication"
            )

            # Chỉ có hình thức xác thực HARD TOKEN mới tốn phí
            has_fee = EBANKING_HAS_FEE if "HARD TOKEN" in [auth_type.name for auth_type in auth_types if
                                                           auth_type.active_flag] else EBANKING_HAS_NO_FEE

            e_banking_info_id = generate_uuid()
            # lưu III
            insert_data.append(EBankingInfo(
                # Thông tin tài khoản
                id=e_banking_info_id,
                customer_id=cif_id,
                method_active_password_id=EBANKING_ACTIVE_PASSWORD_EMAIL
                if account_information.is_confirm_password_by_email
                else EBANKING_ACTIVE_PASSWORD_SMS,
                account_name=account_information.account_name,
                ib_mb_flag=account_information.register_flag,
                method_payment_fee_flag=has_fee,
                # Tùy chọn tài khoản
                active_account_flag=optional_e_banking_account.active_account_flag,
                reset_password_flag=optional_e_banking_account.reset_password_flag,
                note=optional_e_banking_account.note
            ))

            # lưu III -> 4 Hình thức xác thực
            insert_data.extend([EBankingInfoAuthentication(
                e_banking_info_id=e_banking_info_id,
                method_authentication_id=auth_method_id
            ) for auth_method_id in auth_method_ids])

        e_banking_data = self.call_repos(
            await repos_save_e_banking_data(
                session=self.oracle_session,
                cif_id=cif_id,
                insert_data=insert_data,
                created_by=self.current_user.full_name_vn
            )
        )

        return self.response(data=e_banking_data)

    async def ctr_e_banking(self, cif_id: str):
        e_banking_data = self.call_repos(await repos_get_e_banking_data(cif_id))

        return self.response(data=e_banking_data)

    async def ctr_balance_payment_account(self, cif_id: str):
        payment_account_data = self.call_repos(await repos_get_list_balance_payment_account(cif_id))

        return self.response(data=payment_account_data)

    async def get_detail_reset_password(self, cif_id: str):
        detail_reset_password_data = self.call_repos(await repos_get_detail_reset_password(cif_id))

        return self.response(data=detail_reset_password_data)

    async def ctr_balance_saving_account(self, cif_id: str):
        balance_saving_account_data = self.call_repos(await repos_balance_saving_account_data(cif_id))

        return self.response_paging(
            data=balance_saving_account_data,
            total_item=len(balance_saving_account_data)
        )

    async def get_detail_reset_password_teller(self, cif_id: str):
        detail_reset_password_data = self.call_repos(await repos_get_detail_reset_password_teller(cif_id))

        return self.response(data=detail_reset_password_data)
