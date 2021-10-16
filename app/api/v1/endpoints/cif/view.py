from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.controller import CtrCustomer
from app.api.v1.endpoints.cif.schema import CifInformationRes
from app.utils.swagger import swagger_response

router = APIRouter()


@router.get(
    path="/{cif_id}/",
    name="Detail",
    description="Lấy dữ liệu tab `THÔNG TIN CIF` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[CifInformationRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_cif_info(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header()) # noqa
):
    cif_info = await CtrCustomer().ctr_cif_info(cif_id)
    return ResponseData[CifInformationRes](**cif_info)
