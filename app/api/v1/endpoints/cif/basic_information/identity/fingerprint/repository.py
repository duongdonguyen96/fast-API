import json

from sqlalchemy import and_, delete, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.repository import (
    write_transaction_log_and_update_booking
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity, CustomerIdentityImage
)
from app.third_parties.oracle.models.master_data.identity import (
    FingerType, HandSide
)
from app.utils.constant.cif import (
    BUSINESS_FORM_TTCN_GTDD_VT, IMAGE_TYPE_FINGERPRINT
)
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST
from app.utils.functions import now


@auto_commit
async def repos_save_fingerprint(
        cif_id: str,
        identity_id: str,
        log_data: json,
        session: Session,
        list_data_insert: list,
        created_by: str
) -> ReposReturn:
    # lấy list customer_identity_image theo vân tay
    customer_identity_image = session.execute(
        select(
            CustomerIdentityImage.id
        ).filter(
            and_(
                CustomerIdentityImage.identity_id == identity_id,
                CustomerIdentityImage.image_type_id == IMAGE_TYPE_FINGERPRINT
            )
        )
    ).scalars().all()
    # xóa list id vân tay
    if customer_identity_image:
        session.execute(
            delete(
                CustomerIdentityImage
            ).filter(CustomerIdentityImage.id.in_(customer_identity_image))
        )

    session.bulk_save_objects([CustomerIdentityImage(**data_insert) for data_insert in list_data_insert])

    await write_transaction_log_and_update_booking(
        description="Tạo CIF -> Thông tin cá nhân -> Khuôn mặt -- Tạo mới",
        log_data=log_data,
        session=session,
        customer_id=cif_id,
        business_form_id=BUSINESS_FORM_TTCN_GTDD_VT
    )

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_get_data_finger(cif_id: str, session: Session) -> ReposReturn:
    query_data = session.execute(
        select(
            CustomerIdentityImage,
            HandSide,
            FingerType
        ).join(
            CustomerIdentity, and_(
                CustomerIdentityImage.identity_id == CustomerIdentity.id,
                CustomerIdentity.customer_id == cif_id
            )
        ).join(
            HandSide, CustomerIdentityImage.hand_side_id == HandSide.id
        ).join(
            FingerType, CustomerIdentityImage.finger_type_id == FingerType.id
        ).filter(
            CustomerIdentityImage.image_type_id == IMAGE_TYPE_FINGERPRINT
        ).order_by(CustomerIdentityImage.finger_type_id)
    ).all()

    if not query_data:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    return ReposReturn(data=query_data)
