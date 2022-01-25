from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.payment_account.co_owner.controller import (
    CtrConfigCoOwner
)
from app.api.v1.endpoints.config.payment_account.co_owner.schema import (
    ConfigAgreementResponse
)

router = APIRouter()


@router.get(
    path="/agreement/",
    name="Agreement",
    description="Lấy nội dung `Đồng Sở Hữu` -> `D. Thỏa thuận - Ủy quyền`",
    responses=swagger_response(
        response_model=ResponseData[List[ConfigAgreementResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_agreement_info(
        current_user=Depends(get_current_user_from_header())
):
    agreement_info = await CtrConfigCoOwner(current_user).ctr_agreement_info()
    return ResponseData[List[ConfigAgreementResponse]](**agreement_info)
