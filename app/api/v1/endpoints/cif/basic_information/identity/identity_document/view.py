from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.controller import CtrIdentity

from app.api.v1.endpoints.cif.basic_information.identity.identity_document.schema import IdentityCardDetailRes, \
    IdentityCardCreateSuccessRes, CitizenCardCreateSuccessRes, PassportCreateSuccessRes, PassportDocumentReqRes, \
    IdentityCardReqRes, CitizenCardReqRes
from app.utils.swagger import swagger_response

router_special = APIRouter()


# CMND
@router_special.post(
    path="/basic-information/identity/identity-document/identity-card/",
    name="1. GTĐD - A. GTĐD - CMND - Lưu",
    description="Lưu",
    responses=swagger_response(
        response_model=ResponseData[IdentityCardCreateSuccessRes],
        success_status_code=status.HTTP_200_OK
    ),
    tags=['[CIF] I. TTCN']
)
async def view_create(
        identity_card_document_req: IdentityCardReqRes,
        current_user=Depends(get_current_user_from_header())
):
    identity_card_info = await CtrIdentity(current_user).save_identity_document(identity_card_document_req)
    return ResponseData[IdentityCardCreateSuccessRes](**identity_card_info)


router = APIRouter()


@router.get(
    path="/identity-card/",
    name="1. GTĐD - A. GTĐD - CMND - Chi Tiết",
    description="Chi tiết",
    responses=swagger_response(
        response_model=ResponseData[IdentityCardDetailRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_detail_identity_card(
        cif_id: str = Path(...),
        current_user=Depends(get_current_user_from_header())
):
    identity_card_info = await CtrIdentity().detail_identity_document(cif_id)
    return ResponseData[IdentityCardDetailRes](**identity_card_info)


# CCCD
@router_special.post(
    path="/basic-information/identity/identity-document/citizen-card/",
    name="1. GTĐD - A. GTĐD - CCCD",
    description="Lưu",
    responses=swagger_response(
        response_model=ResponseData[CitizenCardCreateSuccessRes],
        success_status_code=status.HTTP_200_OK
    ),
    tags=['[CIF] I. TTCN']
)
async def view_create(
        citizen_card_document_req: CitizenCardReqRes,
        current_user=Depends(get_current_user_from_header())
):
    identity_card_info = await CtrIdentity(current_user).save_identity_document(citizen_card_document_req)
    return ResponseData[IdentityCardCreateSuccessRes](**identity_card_info)


@router.get(
    path="/citizen-card/",
    name="1. GTĐD - A. GTĐD - CCCD - Chi Tiết",
    description="Chi tiết",
    responses=swagger_response(
        response_model=ResponseData[CitizenCardReqRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_detail_citizen_card(
        cif_id: str = Path(...),
        current_user=Depends(get_current_user_from_header())
):
    identity_card_info = await CtrIdentity().detail_identity_document(cif_id)
    return ResponseData[CitizenCardReqRes](**identity_card_info)


# HC
@router_special.post(
    path="/basic-information/identity/identity-document/passport/",
    name="1. GTĐD - A. GTĐD - HC",
    description="Lưu",
    responses=swagger_response(
        response_model=ResponseData[PassportCreateSuccessRes],
        success_status_code=status.HTTP_200_OK
    ),
    tags=['[CIF] I. TTCN']
)
async def view_create(
        passport_document_req: PassportDocumentReqRes,
        current_user=Depends(get_current_user_from_header())
):
    passport_info = await CtrIdentity(current_user).save_identity_document(passport_document_req)
    return ResponseData[PassportCreateSuccessRes](**passport_info)


@router.get(
    path="/passport/",
    name="1. GTĐD - A. GTĐD - HC - Chi Tiết",
    description="Chi tiết",
    responses=swagger_response(
        response_model=ResponseData[PassportDocumentReqRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_detail_passport(
        cif_id: str = Path(...),
        current_user=Depends(get_current_user_from_header())
):
    passport_info = await CtrIdentity().detail_identity_document(cif_id)
    return ResponseData[PassportDocumentReqRes](**passport_info)