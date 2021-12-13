from typing import List

from sqlalchemy import and_, delete, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.basic_information.fatca.model import (
    CustomerFatca, CustomerFatcaDocument
)
from app.third_parties.oracle.models.master_data.others import FatcaCategory
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST


@auto_commit
async def repos_save_fatca_document(
        cif_id: str,
        list_data_insert_fatca_document: List,
        list_data_insert_fatca: List,
        session: Session,
) -> ReposReturn:
    # list fatca_id cần xóa trong bảng fatca_document
    customer_fatca_id = session.execute(
        select(
            CustomerFatca.id
        ).filter(CustomerFatca.customer_id == cif_id)
    ).scalars().all()

    session.execute(
        delete(
            CustomerFatcaDocument
        ).filter(CustomerFatcaDocument.customer_fatca_id.in_(customer_fatca_id))
    )
    session.execute(
        delete(
            CustomerFatca
        ).filter(CustomerFatca.customer_id == cif_id)
    )

    fatca_data = [CustomerFatca(**data_insert) for data_insert in list_data_insert_fatca]
    session.bulk_save_objects(fatca_data)

    fatca_document_data = [CustomerFatcaDocument(**data_insert) for data_insert in list_data_insert_fatca_document]
    session.bulk_save_objects(fatca_document_data)

    return ReposReturn(data={
        "cif_id": cif_id
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

    return ReposReturn(data=query_data_fatca)
