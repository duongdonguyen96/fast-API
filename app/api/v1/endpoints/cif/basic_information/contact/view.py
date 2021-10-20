from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.contact.controller import (
    CtrContactInformation
)
from app.api.v1.endpoints.cif.basic_information.contact.schema import (
    ContactInformationDetailResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="3. Thông tin liên lạc",
    description="I. TTCN - Thông tin liên lạc - Chi tiết",
    responses=swagger_response(
        response_model=ContactInformationDetailResponse,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_detail(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    ctr_contact_information = CtrContactInformation(current_user)

    contact_information_detail = await ctr_contact_information.detail_contact_information(cif_id=cif_id)

    return ResponseData[ContactInformationDetailResponse](**contact_information_detail)
