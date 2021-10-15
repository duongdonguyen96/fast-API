from fastapi import APIRouter, Depends, Path
from pydantic.generics import GenericModel
from starlette import status

from app.api.base.response import ResponseData
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.controller import CtrIdentity
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.repository import TYPE_PASSPORT, \
    TYPE_CITIZEN_CARD, TYPE_IDENTITY_CARD
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.schema import PassportRes, \
    CitizenCardDocumentRes, IdentityCardDocumentRes
from app.api.v1.endpoints.user.schema import UserInfoRes
from app.utils.swagger import swagger_response

router_special = APIRouter()


@router_special.post(
    path="/basic-information/identity/identity-document/",
    name="1. GTĐD - A. GTĐD",
    description="Create",
    responses=swagger_response(
        response_model=ResponseData[UserInfoRes],
        success_status_code=status.HTTP_200_OK
    ),
    tags=['[CIF] I. TTCN']
)
async def view_create_identity_document(current_user=Depends(get_current_user_from_header())):
    data = {}
    return ResponseData[UserInfoRes](**data)


router = APIRouter()


@router.get(
    path="/",
    name="1. GTĐD - A. GTĐD - Chi tiết",
    description="Chi tiết",
    responses=swagger_response(
        response_model=ResponseData[CitizenCardDocumentRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_detail(
        identity_document_type: int,
        cif_id: str = Path(...),
        current_user=Depends(get_current_user_from_header())
):
    data = await CtrIdentity().detail(cif_id, identity_document_type)
    if identity_document_type == TYPE_IDENTITY_CARD:
        return ResponseData[IdentityCardDocumentRes](**data)
    elif identity_document_type == TYPE_CITIZEN_CARD:
        return ResponseData[CitizenCardDocumentRes](**data)
    else:
        return ResponseData[PassportRes](**data)