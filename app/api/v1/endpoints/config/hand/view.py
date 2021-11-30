from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.hand.controller import CtrConfigHand
from app.api.v1.schemas.utils import DropdownResponse

router = APIRouter()


@router.get(
    path="/hand-side/",
    name="Hand Side",
    description="Lấy dữ liệu bàn tay",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_hand_side_info(
        current_user=Depends(get_current_user_from_header())
):
    hand_side_info = await CtrConfigHand(current_user).ctr_hand_side_info()
    return ResponseData[List[DropdownResponse]](**hand_side_info)


@router.get(
    path="/finger-printer/",
    name="Finger Printer",
    description="Lấy dữ liệu các loại vân tay",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_finger_printer_info(
        current_user=Depends(get_current_user_from_header())
):
    finger_printer_info = await CtrConfigHand(current_user).ctr_finger_printer()
    return ResponseData[List[DropdownResponse]](**finger_printer_info)
