from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.cif.basic_information.fatca.schema import (
    FatcaRequest
)
from app.third_parties.oracle.models.cif.basic_information.fatca.model import (
    CustomerFatca, CustomerFatcaDocument
)
from app.third_parties.oracle.models.master_data.others import FatcaCategory
from app.utils.constant.cif import (
    CIF_ID_TEST, LANGUAGE_TYPE_EN, LANGUAGE_TYPE_VI
)
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import now


async def repos_save_fatca(cif_id: str, fatca: FatcaRequest, created_by: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_get_fatca_data(cif_id: str, session: Session) -> ReposReturn:
    query_data_fatca = session.execute(
        select(
            CustomerFatca,
            FatcaCategory,
            CustomerFatcaDocument
        ).join(
            FatcaCategory, and_(
                CustomerFatca.fatca_category_id == FatcaCategory.id,
                CustomerFatca.customer_id == cif_id
            )
        ).outerjoin(
            CustomerFatcaDocument, CustomerFatca.id == CustomerFatcaDocument.customer_fatca_id
        ).order_by(FatcaCategory.order_no)
    ).all()

    if not query_data_fatca:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    fatca_information = {}

    for customer_fatca, fatca_category, customer_fatca_document in query_data_fatca:
        if fatca_category.id not in fatca_information:
            fatca_information[fatca_category.id] = {
                "id": fatca_category.id,
                "code": fatca_category.code,
                "name": fatca_category.name,
                "select_flag": customer_fatca.value,
                "document_depend_language": {}
            }
        # check customer_fatca_document
        if customer_fatca_document is not None:
            document = {
                "id": customer_fatca_document.id,
                "name": customer_fatca_document.document_name,
                "url": customer_fatca_document.document_url,
                "active_flag": customer_fatca_document.active_flag,
                "version": customer_fatca_document.document_version,
                "content_type": "Word",  # TODO
                "size": "1MB",  # TODO
                "folder_name": "Khởi tạo CIF",  # TODO
                "created_by": "Nguyễn Phúc",  # TODO
                "created_at": customer_fatca_document.created_at,
                "updated_by": "Trần Bình Liên",  # TODO
                "updated_at": "2020-12-30 06:07:08",  # TODO
                "note": "Tài liệu quan trọng"  # TODO
            }

            if customer_fatca_document.document_language_type == LANGUAGE_TYPE_EN:
                fatca_information[fatca_category.id]["document_depend_language"][LANGUAGE_TYPE_EN] = document

            if customer_fatca_document.document_language_type == LANGUAGE_TYPE_VI:
                fatca_information[fatca_category.id]["document_depend_language"][LANGUAGE_TYPE_VI] = document

    # TODO : xét cứng dữ liệu language -> chưa thấy table lưu
    en_documents = []
    vi_documents = []
    for fatca_category_id, fatca_category_data in fatca_information.items():
        en_document = fatca_category_data['document_depend_language'].get(LANGUAGE_TYPE_EN)
        vi_document = fatca_category_data['document_depend_language'].get(LANGUAGE_TYPE_VI)

        en_documents.append(
            {
                "id": fatca_category_data['id'],
                "code": fatca_category_data['code'],
                "name": fatca_category_data['name'],
                "document": en_document
            }
        )

        vi_documents.append(
            {
                "id": fatca_category_data['id'],
                "code": fatca_category_data['code'],
                "name": fatca_category_data['name'],
                "document": vi_document
            }
        )

    return ReposReturn(data={
        "fatca_information": list(fatca_information.values()),
        "document_information": [
            {
                "language_type": {
                    "id": "1",
                    "code": LANGUAGE_TYPE_VI,
                    "name": "vn"
                },
                "documents": vi_documents
            },
            {
                "language_type": {
                    "id": "2",
                    "code": LANGUAGE_TYPE_EN,
                    "name": "en"
                },
                "documents": en_documents
            }
        ]
    })
