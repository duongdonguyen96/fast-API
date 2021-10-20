from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.guardian.controller import (
    CtrGuardian
)
from app.api.v1.endpoints.cif.basic_information.guardian.schema import (
    DetailGuardianResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="I. TTCN - Thông tin người giám hộ",
    description="Chi tiết",
    responses=swagger_response(
        response_model=ResponseData[DetailGuardianResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_detail(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    ctr_identity_document = CtrGuardian(current_user)

    identity_document_info = await ctr_identity_document.detail(
        cif_id=cif_id
    )

    return ResponseData[DetailGuardianResponse](
        **identity_document_info
    )
