from typing import List

from fastapi import APIRouter, Depends, Path, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.debit_card.controller import CtrDebitCard
from app.api.v1.endpoints.cif.debit_card.schema import (
    DebitCardRequest, DebitCardResponse, ListCardTypeResponse
)
from app.api.v1.schemas.utils import SaveSuccessResponse

router = APIRouter()


@router.get(
    path="/",
    name="Detail Debit Card",
    description="Lấy dữ liệu tab `V. THẺ GHI NỢ` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[DebitCardResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_debit_card(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    debit_card = await CtrDebitCard(current_user).ctr_debit_card(cif_id)
    return ResponseData[DebitCardResponse](**debit_card)


@router.post(
    path="/",
    name="Chi tiết thẻ ghi nợ",
    description="Lưu dữ liệu tab `V. THẺ GHI NỢ` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[DebitCardRequest],
        success_status_code=status.HTTP_200_OK,
    ),
)
async def view_add_debit_card(
        debt_card_req: DebitCardRequest,  # TODO: Thêm example
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    add_debt_card = await CtrDebitCard(current_user).ctr_add_debit_card(cif_id, debt_card_req)
    return ResponseData[SaveSuccessResponse](**add_debt_card)


@router.get(
    path="/release-parameters/",
    name="Get list debit card type",
    description="Lấy dữ liệu tab `V THẺ GHI NỢ - 9. DANH SÁCH THÔNG TIN PHÁT HÀNH`",
    responses=swagger_response(
        response_model=ResponseData[List[ListCardTypeResponse]],
        success_status_code=status.HTTP_200_OK,
    ),
)
async def view_list_debit_card_type(
        branch_of_card_id: str = Query(..., description="id thương hiệu thẻ"),
        issuance_fee_id: str = Query(..., description="id phí phát hành"),
        annual_fee_id: str = Query(..., description="id phí hằng năm"),
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    list_debit_card_type = await CtrDebitCard(
        current_user
    ).ctr_list_debit_card_type(
        cif_id,
        branch_of_card_id,
        issuance_fee_id,
        annual_fee_id
    )
    return ResponseData[List[ListCardTypeResponse]](**list_debit_card_type)
