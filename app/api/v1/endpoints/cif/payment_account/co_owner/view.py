from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.payment_account.co_owner.controller import (
    CtrCoOwner
)
from app.api.v1.endpoints.cif.payment_account.co_owner.schema import (
    AccountHolderSuccessResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="B. Thông tin đồng sở hữu",
    description="Lấy dữ liệu tab `THÔNG TIN ĐỒNG SỞ HỮU` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[AccountHolderSuccessResponse],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_retrieve_co_owner(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    co_owner_data = await CtrCoOwner(current_user).ctr_co_owner(cif_id)
    return ResponseData[AccountHolderSuccessResponse](**co_owner_data)
