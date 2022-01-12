from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.fatca.controller import CtrConfigFatca
from app.api.v1.schemas.utils import DropdownResponse

router = APIRouter()


@router.get(
    path="/fatca/",
    name="fatca",
    description="Lấy dữ liệu fatca",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_fatca_info(
        current_user=Depends(get_current_user_from_header())
):
    gender_info = await CtrConfigFatca(current_user).ctr_fatca_info()
    return ResponseData[List[DropdownResponse]](**gender_info)
