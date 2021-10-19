from typing import List

from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.identity.face.controller import (
    CtrFace
)
from app.api.v1.endpoints.cif.basic_information.identity.face.schema import (
    FacesResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="1. GTĐD - B. Khuôn mặt",
    description="Lấy dữ liệu tab `KHUÔN MẶT` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[List[FacesResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_face(
        cif_id: str = Path(...),
        current_user=Depends(get_current_user_from_header())
):
    face_info = await CtrFace(current_user).ctr_get_list_face(cif_id)
    return ResponseData[List[FacesResponse]](**face_info)
