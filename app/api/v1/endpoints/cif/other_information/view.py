from fastapi import APIRouter, Body, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.other_information.controller import CtrOtherInfo
from app.api.v1.endpoints.cif.other_information.schema import (
    EXAMPLE_REQUEST_UPDATE_OTHER_INFO,
    EXAMPLE_RESPONSE_SUCCESS_UPDATE_OTHER_INFO, OtherInformationResponse,
    OtherInformationUpdateRequest, OtherInformationUpdateResponse
)
from app.utils.swagger import swagger_response

router = APIRouter()


@router.get(
    path="/",
    name="Detail",
    description="Lấy dữ liệu tab `II. THÔNG TIN KHÁC` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[OtherInformationResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_other_info(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    other_info = await CtrOtherInfo(current_user).ctr_other_info(cif_id)
    return ResponseData[OtherInformationResponse](**other_info)


@router.put(
    path="/",
    name="Update",
    description="Cập nhật dữ liệu tab `II. THÔNG TIN KHÁC` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[OtherInformationUpdateResponse],
        success_status_code=status.HTTP_200_OK,
        success_examples=EXAMPLE_RESPONSE_SUCCESS_UPDATE_OTHER_INFO
    ),
)
async def view_update_other_info(
        cif_id: str = Path(..., description='Id CIF ảo'),
        update_other_info_req: OtherInformationUpdateRequest = Body(
            ...,
            examples=EXAMPLE_REQUEST_UPDATE_OTHER_INFO,
        ),
        current_user=Depends(get_current_user_from_header())
):
    update_other_info = await CtrOtherInfo(current_user).ctr_update_other_info(cif_id, update_other_info_req)
    return ResponseData[OtherInformationUpdateResponse](**update_other_info)
