from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.user.schema import UserInfoResponse
from app.utils.swagger import swagger_response

router = APIRouter()


@router.post(
    path="/",
    name="1. GTĐD - E. GTĐD phụ",
    description="Create",
    responses=swagger_response(
        response_model=ResponseData[UserInfoResponse],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_create_identity_document(current_user=Depends(get_current_user_from_header())):
    data = {}
    return ResponseData[UserInfoResponse](**data)


@router.get(
    path="/",
    name="1. GTĐD - E. GTĐD phụ",
    description="Detail",
    responses=swagger_response(
        response_model=ResponseData[UserInfoResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_user(
        cif_id: str = Path(...),
        current_user=Depends(get_current_user_from_header())
):
    data = {'cif_id': cif_id}
    return ResponseData[UserInfoResponse](**data)
