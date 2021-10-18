from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.other_information.controller import CtrOtherInfo
from app.api.v1.endpoints.cif.other_information.schema import (
    OtherInformationResponse
)
from app.utils.swagger import swagger_response

router = APIRouter()


@router.get(
    path="/",
    name="Detail",
    description="Lấy dữ liệu tab `THÔNG TIN KHÁC` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[OtherInformationResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_cif_info(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header()) # noqa
):
    other_info = await CtrOtherInfo().ctr_other_info(cif_id)
    return ResponseData[OtherInformationResponse](**other_info)
