from typing import List

from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.e_banking.controller import CtrEBanking
from app.api.v1.endpoints.cif.e_banking.schema import (
    BalanceSavingAccountsResponse, EBankingResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="E-banking",
    description="Lấy dữ liệu tab `E BANKING` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[EBankingResponse],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_retrieve_e_banking(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    e_banking_data = await CtrEBanking(current_user).ctr_e_banking(cif_id)
    return ResponseData[EBankingResponse](**e_banking_data)


@router.get(
    path="/balance-saving-account/",
    name="Danh sách tài khoản tiết kiệm",
    description="Lấy dữ liệu `DANH SÁCH TÀI KHOẢN TIẾT KIỆM`",
    responses=swagger_response(
        response_model=ResponseData[List[BalanceSavingAccountsResponse]],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_balance_saving_account(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    balance_saving_account_data = await CtrEBanking(current_user).ctr_balance_saving_account(cif_id)
    return ResponseData[List[BalanceSavingAccountsResponse]](**balance_saving_account_data)
