from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.controller import (
    CtrFingerPrint
)
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.schema import (
    FingerReq
)
from app.api.v1.endpoints.user.schema import UserInfoRes
from app.utils.swagger import swagger_response

router = APIRouter()


@router.post(
    path="/",
    name="1. GTĐD - C. Vân tay",
    description="Create",
    status_code=status.HTTP_201_CREATED,
    responses=swagger_response(
        response_model=ResponseData[FingerReq],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_create_identity_document(finger_req: FingerReq):
    data = await CtrFingerPrint().ctr_save_fingerprint(finger_req)
    return ResponseData[FingerReq](**data)


@router.get(
    path="/",
    name="1. GTĐD - C. Vân tay",
    description="Detail",
    responses=swagger_response(
        response_model=ResponseData[UserInfoRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_user(
        cif_id: str = Path(...),
        current_user=Depends(get_current_user_from_header())
):
    data = {'cif_id': cif_id}
    return ResponseData[UserInfoRes](**data)
