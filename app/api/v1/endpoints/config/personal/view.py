from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.personal.controller import CtrConfigPersonal
from app.api.v1.schemas.utils import DropdownResponse

router = APIRouter()


@router.get(
    path="/gender/",
    name="Gender",
    description="Lấy dữ liệu giới tính",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gender_info(
        current_user=Depends(get_current_user_from_header())
):
    gender_info = await CtrConfigPersonal(current_user).ctr_gender_info()
    return ResponseData[List[DropdownResponse]](**gender_info)


@router.get(
    path="/nationality/",
    name="Nationality",
    description="Lấy dữ liệu quốc tịch",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_nationality_info(
        current_user=Depends(get_current_user_from_header())
):
    nationality_info = await CtrConfigPersonal(current_user).ctr_nationality_info()
    return ResponseData[List[DropdownResponse]](**nationality_info)


@router.get(
    path="/ethnic/",
    name="Ethnic",
    description="Lấy dữ liệu dân tộc ",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_ethnic_info(
        current_user=Depends(get_current_user_from_header())
):
    ethnic_info = await CtrConfigPersonal(current_user).ctr_ethnic_info()
    return ResponseData[List[DropdownResponse]](**ethnic_info)


@router.get(
    path="/religion/",
    name="Religion",
    description="Lấy dữ liệu tôn giáo ",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_religion_info(
        current_user=Depends(get_current_user_from_header())
):
    religion_info = await CtrConfigPersonal(current_user).ctr_religion_info()
    return ResponseData[List[DropdownResponse]](**religion_info)


@router.get(
    path="/honorific/",
    name="Honorific",
    description="Lấy dữ liệu danh xưng ",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_honorific_info(
        current_user=Depends(get_current_user_from_header())
):
    honorific_info = await CtrConfigPersonal(current_user).ctr_honorific_info()
    return ResponseData[List[DropdownResponse]](**honorific_info)
