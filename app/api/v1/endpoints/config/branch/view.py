from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.branch.controller import CtrBranch
from app.api.v1.schemas.utils import DropdownResponse

router = APIRouter()


@router.get(
    path="/scb-branch/",
    name="SCB Branch",
    description="Lấy dữ liệu chi nhánh SCB",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_branch_info(
        current_user=Depends(get_current_user_from_header()),
        region_id: Optional[str] = Query(None, description="`ID khu vực`"),
        province_id: Optional[str] = Query(None, description="`ID Tỉnh`"),
        district_id: Optional[str] = Query(None, description="`ID Quận/Huyện`"),
        ward_id: Optional[str] = Query(None, description="`ID Phường/Xã`"),
):
    branch_info = await CtrBranch(current_user).ctr_branch_info(
        region_id=region_id,
        province_id=province_id,
        district_id=district_id,
        ward_id=ward_id
    )
    return ResponseData[List](**branch_info)
