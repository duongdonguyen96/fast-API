from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.controller import (
    CtrBasicInformation
)
from app.api.v1.endpoints.cif.basic_information.schema import (
    DetailRelationshipResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="GTĐD - Thông tin khách hàng khác",
    description="Chi tiết người giám hộ hoặc người có quan hệ với khách hàng qua mã CIF",
    responses=swagger_response(
        response_model=ResponseData[DetailRelationshipResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_detail_relationship(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    """
    relationship là tên dùng chung cho Mối quan hệ khách hàng và Người giám hộ
    Trả về thông tin chi tiết của người có liên quan tới người hiện hành thông qua CIF_ID
    """
    ctr_basic_information = CtrBasicInformation(current_user)

    detail_basic_information = await ctr_basic_information.detail_relationship(
        cif_id=cif_id
    )

    return ResponseData[DetailRelationshipResponse](
        **detail_basic_information
    )
