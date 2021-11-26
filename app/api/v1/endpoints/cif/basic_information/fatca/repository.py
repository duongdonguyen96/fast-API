from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.fatca.model import (
    CustomerFatca, CustomerFatcaDocument
)
from app.third_parties.oracle.models.master_data.others import FatcaCategory
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import now


async def repos_get_fatca_category_ids(fatca_category_ids: List[str], session: Session) -> ReposReturn:
    crm_fatca_category = session.execute(
        select(
            FatcaCategory
        ).filter(FatcaCategory.id.in_(fatca_category_ids))
    ).scalars().all()

    if len(crm_fatca_category) != len(fatca_category_ids):
        return ReposReturn(is_error=True, detail="fatca category is not exist", loc="fatca category id")

    return ReposReturn(data=crm_fatca_category)


async def repos_save_fatca(list_data_insert_fatca: List, session: Session) -> ReposReturn:
    data_insert = [CustomerFatca(**data_insert) for data_insert in list_data_insert_fatca]
    session.bulk_save_objects(data_insert)

    return ReposReturn(data=data_insert)


async def repos_get_fatca_customer(cif_id: str, session: Session) -> ReposReturn:
    crm_customer_fatca = session.execute(
        select(
            CustomerFatca
        ).filter(CustomerFatca.customer_id == cif_id)
    ).scalars().all()

    return ReposReturn(data=crm_customer_fatca)


async def repos_save_fatca_document(
        cif_id: str,
        list_data_insert_fatca_document: List,
        session: Session,
        created_by: str
) -> ReposReturn:

    data_insert = [CustomerFatcaDocument(**data_insert) for data_insert in list_data_insert_fatca_document]
    session.bulk_save_objects(data_insert)
    session.commit()

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_get_fatca_data(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "fatca_information": [
            {
                "id": "1",
                "code": "code",
                "name": "Quý khác là công dân Hoa Kỳ hoặc thường trú hợp pháp tại Hoa Kỳ(có thẻ xanh)",
                "active_flag": True
            },
            {
                "id": "2",
                "code": "code",
                "name": "Quý khách có sinh ra tại Hoa Kỳ không",
                "active_flag": False
            },
            {
                "id": "3",
                "code": "code",
                "name": "Quý khách có thư ủy quyền hoặc ủy quyền cho "
                        "một cá nhân/tổ chức có địa chỉ tại Hoa Kỳ không",
                "active_flag": True
            },
            {
                "id": "4",
                "code": "code",
                "name": "Quý khách có lệnh chuyển tiền tới tài khoản tại Hoa Kỳ "
                        "hoặc khoản tiền nhận được thường xuyên từ một địa chỉ Hoa Kỳ không",
                "active_flag": True
            },
            {
                "id": "5",
                "code": "code",
                "name": "Quý khách có địa chỉ thư tín (bao gồm hộp thư bưu điện)"
                        " hoặc nơi cư trú hiện tại ở Hoa Kỳ hoặc số điện thoại Hoa Kỳ",
                "active_flag": True
            },
            {
                "id": "6",
                "code": "code",
                "name": "Quý khách có địa chỉ “nhờ chuyển thư” hoặc “giữ thư” tại Hoa Kỳ",
                "active_flag": False
            }
        ],
        "document_information": [
            {
                "language_type": {
                    "id": "1",
                    "code": "VN",
                    "name": "vn"
                },
                "documents": [
                    {
                        "id": "1",
                        "name": "W-8BEN",
                        "url": "url-w8ben",
                        "active_flag": True,
                        "version": "1.0",
                        "content_type": "Word",
                        "size": "1MB",
                        "folder_name": "Khởi tạo CIF",
                        "created_by": "Nguyễn Phúc",
                        "created_at": "2020-12-29 06:07:08",
                        "updated_by": "Trần Bình Liên",
                        "updated_at": "2020-12-30 06:07:08",
                        "note": "Tài liệu quan trọng"
                    },
                    {
                        "id": "2",
                        "name": "W-8BEN",
                        "url": "url-w8ben",
                        "active_flag": True,
                        "version": "1.0",
                        "content_type": "Word",
                        "size": "1MB",
                        "folder_name": "Khởi tạo CIF",
                        "created_by": "Nguyễn Phúc",
                        "created_at": "2020-12-28 06:07:08",
                        "updated_by": "Trần Bình Liên",
                        "updated_at": "2020-12-29 06:07:08",
                        "note": "Tài liệu quan trọng"
                    }
                ]
            },
            {
                "language_type": {
                    "id": "2",
                    "code": "EN",
                    "name": "en"
                },
                "documents": [
                    {
                        "id": "3",
                        "name": "W-8BEN",
                        "url": "url-w8ben",
                        "active_flag": True,
                        "version": "1.0",
                        "content_type": "Word",
                        "size": "1MB",
                        "folder_name": "Khởi tạo CIF",
                        "created_by": "Nguyễn Phúc",
                        "created_at": "2020-12-27 06:07:08",
                        "updated_by": "Trần Bình Liên",
                        "updated_at": "2020-12-28 06:07:08",
                        "note": "import document"
                    },
                    {
                        "id": "4",
                        "name": "W-8BEN",
                        "url": "url-w8ben",
                        "active_flag": True,
                        "version": "1.0",
                        "content_type": "Word",
                        "size": "1MB",
                        "folder_name": "Khởi tạo CIF",
                        "created_by": "Nguyễn Phúc",
                        "created_at": "2020-12-26 06:07:08",
                        "updated_by": "Trần Bình Liên",
                        "updated_at": "2020-12-27 06:07:08",
                        "note": "import document"
                    }
                ]
            }
        ]
    })
