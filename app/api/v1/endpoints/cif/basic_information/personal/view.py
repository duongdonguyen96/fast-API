from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.personal.controller import (
    CtrPersonal
)
from app.api.v1.endpoints.cif.basic_information.personal.schema import (
    PersonalRequest, PersonalSaveSuccessResponse, PersonalSuccessResponse
)

router = APIRouter()


@router.post(
    path="/",
    name="2. Thông tin cá nhân",
    description="Tạo dữ liệu tab `THÔNG TIN CÁ NHÂN` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[PersonalSaveSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_create_personal(
        personal: PersonalRequest,
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    personal_data_request = await CtrPersonal(current_user).ctr_save_personal(cif_id, personal)
    return ResponseData[PersonalSaveSuccessResponse](**personal_data_request)


@router.get(
    path="/",
    name="1 TTCN",
    description="Lấy dữ liệu tab `THÔNG TIN CÁ NHÂN` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[PersonalSuccessResponse],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_retrieve_personal(
        cif_id: str = Path(...),
        current_user=Depends(get_current_user_from_header())
):
    personal_data = await CtrPersonal(current_user).ctr_personal(cif_id)
    return ResponseData[PersonalSuccessResponse](**personal_data)
