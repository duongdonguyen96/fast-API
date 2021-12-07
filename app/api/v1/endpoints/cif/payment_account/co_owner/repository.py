from typing import List

from sqlalchemy import and_, delete, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount, JointAccountHolder, JointAccountHolderAgreementAuthorization
)
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import now


async def repos_check_list_cif_number(list_cif_number_request: list, session: Session) -> ReposReturn:
    list_customer = session.execute(
        select(
            Customer
        ).filter(Customer.cif_number.in_(list_cif_number_request))
    ).all()

    if not list_customer:
        return ReposReturn(is_error=True, msg='CIF_NUMBER_NOT_EXIT')

    return ReposReturn(data=list_customer)


async def repos_get_casa_account(cif_id: str, session: Session) -> ReposReturn:
    casa_account = session.execute(
        select(
            CasaAccount.id
        ).filter(CasaAccount.customer_id == cif_id)
    ).scalar()

    return ReposReturn(data=casa_account)


@auto_commit
async def repos_save_co_owner(
        cif_id: str,
        save_account_holder: List,
        save_account_agree: List,
        session: Session,
        created_by: str
) -> ReposReturn:

    # lấy danh sách account holder để xóa
    account_holder_ids = session.execute(
        select(
            JointAccountHolder.id
        ).join(
            CasaAccount, and_(
                JointAccountHolder.casa_account_id == CasaAccount.id,
                CasaAccount.customer_id == cif_id
            )
        )
    ).scalars().all()

    # xóa JointAccountHolderAgreementAuthorization
    session.execute(
        delete(
            JointAccountHolderAgreementAuthorization
        ).filter(
            JointAccountHolderAgreementAuthorization.joint_account_holder_id.in_(account_holder_ids)
        )
    )

    # xóa account holder
    session.execute(
        delete(
            JointAccountHolder
        ).filter(JointAccountHolder.id.in_(account_holder_ids))
    )

    session.bulk_save_objects([JointAccountHolder(**data_insert) for data_insert in save_account_holder])

    session.bulk_save_objects(
        [JointAccountHolderAgreementAuthorization(**data_insert) for data_insert in save_account_agree])

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_get_co_owner_data(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "joint_account_holder_flag": True,
        "number_of_joint_account_holder": 3,
        "joint_account_holders": [
            {
                "id": "1",
                "full_name_vn": "Trần Ngọc An",
                "basic_information": {
                    "cif_number": "0298472",
                    "customer_relationship": {
                        "id": "1",
                        "code": "code",
                        "name": "Chị gái"
                    },
                    "full_name_vn": "TRẦN NGỌC AN",
                    "date_of_birth": "1990-02-20",
                    "gender": {
                        "id": "1",
                        "code": "Code",
                        "name": "Nữ"
                    },
                    "nationality": {
                        "id": "1",
                        "code": "Code",
                        "name": "Việt Nam"
                    },
                    "mobile_number": "08675968221",
                    "signature_1": {
                        "id": "1",
                        "code": "code",
                        "name": "mẫu chứ ký 1",
                        "image_url": "https://example.com/abc.png"
                    },
                    "signature_2": {
                        "id": "2",
                        "code": "code",
                        "name": "mẫu chứ ký 2",
                        "image_url": "https://example.com/abc.png"
                    }
                },
                "identity_document": {
                    "identity_number": "254136582",
                    "issued_date": "1990-02-20",
                    "expired_date": "1990-02-20",
                    "place_of_issue": {
                        "id": "1",
                        "code": "code",
                        "name": "TP. Hồ Chí Minh"
                    }
                },
                "address_information": {
                    "content_address": "48 Phó Cơ Điều, Phường 12, Quận 5, Thành phố Hồ Chí Minh",
                    "resident_address": "6, Q.6, 279 Lê Quang Sung, Phường 6, Quận 6, Thành phố Hồ Chí Minh"
                }
            }
        ],
        "agreement_authorization": [
            {
                "id": "1",
                "code": "code",
                "content": "Rút tiền (tiền mặt/chuyển khoản) tại quầy; Đề nghị SCB cung "
                           "ứng Séc trắng và nhận Séc trắng tại SCB; Phát hành Séc;"
                           " Đóng tài khoản (bao gồm Thẻ ghi Nợ và dịch vụ Ngân hàng điện tử kết nối với tài khoản)"
                           " và xử lý số dư sau khi đóng tài khoản; Xác nhận số dư tài khoản; "
                           "Tạm khóa/Phong tỏa tài khoản; Đề nghị SCB phát hành Thẻ ghi Nợ kết nối với "
                           "tài khoản thanh toán chung tại SCB.",
                "agreement_flag": True,
                "method_sign": {
                    "id": "1",
                    "code": "code",
                    "name": "Phương thức 3"
                },
                "signature_list": [
                    {
                        "id": "1",
                        "full_name_vn": "Nguyễn Anh Đào"
                    },
                    {
                        "id": "2",
                        "full_name_vn": "Lê Văn A"
                    }
                ]
            },
            {
                "id": "2",
                "code": "code2",
                "content": "Giao dịch chấm dứt tạm khóa, chấm dứt phong tỏa tài khoản và các giao dịch phát sinh khác "
                           "ngoài nội dung nêu tại Nội dung 1: Chữ ký của tất cả các đồng chủ tài khoản.",
                "agreement_flag": True,
                "method_sign": {
                    "id": "1",
                    "code": "code",
                    "name": "Phương thức 2"
                },
                "signature_list": []
            }
        ]
    })


async def repos_detail_co_owner(cif_id: str, cif_number_need_to_find: str):
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    return ReposReturn(data={
        "id": "1",
        "basic_information": {
            "full_name_vn": "TRẦN NGỌC AN",
            "cif_number": "0298472",
            "customer_relationship": {
                "id": "1",
                "code": "code",
                "name": "Chị gái"
            },
            "date_of_birth": "1990-02-20",
            "gender": {
                "id": "1",
                "code": "Code",
                "name": "Nữ"
            },
            "nationality": {
                "id": "1",
                "code": "Code",
                "name": "Việt Nam"
            },
            "mobile_number": "08675968221",
            "signature_1": {
                "id": "1",
                "code": "code",
                "name": "mẫu chứ ký 1",
                "image_url": "https://example.com/abc.png"
            },
            "signature_2": {
                "id": "2",
                "code": "code",
                "name": "mẫu chứ ký 2",
                "image_url": "https://example.com/abc.png"
            }
        },
        "identity_document": {
            "identity_number": "254136582",
            "issued_date": "1990-02-20",
            "expired_date": "1990-02-20",
            "place_of_issue": {
                "id": "1",
                "code": "code",
                "name": "TP. Hồ Chí Minh"
            }
        },
        "address_information": {
            "content_address": "48 Phó Cơ Điều, Phường 12, Quận 5, Thành phố Hồ Chí Minh",
            "resident_address": "6, Q.6, 279 Lê Quang Sung, Phường 6, Quận 6, Thành phố Hồ Chí Minh"
        }
    })
