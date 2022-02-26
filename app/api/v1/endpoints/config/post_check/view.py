from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.post_check.controller import CtrPostCheck
from app.api.v1.schemas.utils import DropdownResponse

router = APIRouter()


@router.get(
    path="/post-check/transaction-status/",
    name="Trạng thái giao dịch hậu kiểm",
    description="Trạng thái giao dịch hậu kiểm",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_transaction_status(
        current_user=Depends(get_current_user_from_header())  # noqa
):
    transaction_status = await CtrPostCheck().ctr_transaction_status()

    return ResponseData[List[DropdownResponse]](**transaction_status)


@router.get(
    path="/post-check/approve-status/",
    name="Trạng thái phê duyệt hậu kiểm",
    description="Trạng thái phê duyệt hậu kiểm",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_approve_status(
        current_user=Depends(get_current_user_from_header())  # noqa
):
    transaction_status = await CtrPostCheck().ctr_approve_status()

    return ResponseData[List[DropdownResponse]](**transaction_status)


@router.get(
    path="/transactions-type/",
    name="Loại giao dịch (Nghiệp vụ)",
    description="Loại giao dịch (Nghiệp vụ)",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_transaction_type(
        current_user=Depends(get_current_user_from_header())  # noqa
):
    transaction_status = await CtrPostCheck().ctr_transaction_type()

    return ResponseData[List[DropdownResponse]](**transaction_status)
