from typing import List

from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.profile_history.controller import (
    CtrProfileHistory
)
from app.api.v1.endpoints.cif.profile_history.schema import (
    CifProfileHistoryResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="Detail",
    description="Lấy dữ liệu tab `LỊCH SỬ HỒ SƠ` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[List[CifProfileHistoryResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_profile_history(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    profile_history = await CtrProfileHistory(current_user).ctr_profile_history(cif_id)
    return ResponseData[List[CifProfileHistoryResponse]](**profile_history)
