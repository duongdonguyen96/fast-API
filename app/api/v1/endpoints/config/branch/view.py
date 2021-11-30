from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.branch.controller import CtrBranch
from app.api.v1.endpoints.config.branch.schema import BranchDropdownResponse

router = APIRouter()


@router.get(
    path="/scb-branch/",
    name="SCB Branch",
    description="Lấy dữ liệu chi nhánh SCB",
    responses=swagger_response(
        response_model=ResponseData[List[BranchDropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_branch_info(
        current_user=Depends(get_current_user_from_header()),
        region_id: Optional[str] = Query(None, description="`id khu vực`")
):
    branch_info = await CtrBranch(current_user).ctr_branch_info(region_id=region_id)
    return ResponseData[List[BranchDropdownResponse]](**branch_info)
