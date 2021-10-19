from typing import Any, List

from fastapi import APIRouter, File, Query, UploadFile
from fastapi.params import Body
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.endpoints.config.file_utils.ctr_file import CtrFileUtils
from app.api.v1.endpoints.schema import (
    CheckFileRes, FileBDSServiceRes, FileDBSServiceDownloadRes
)

router = APIRouter()


@router.post(
    path="/upload/",
    description="Upload file",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=ResponseData[FileBDSServiceRes],
        success_description=status.HTTP_200_OK
    )
)
async def view_file_upload(
        file: UploadFile = File(...)
):
    ctr_file = CtrFileUtils()
    res = await ctr_file.upload_file(file)
    return ResponseData[FileBDSServiceRes](**res)


@router.post(
    path="/multi-upload/",
    description="Upload multi file",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=ResponseData[List[FileBDSServiceRes]],
        success_description=status.HTTP_200_OK
    )
)
async def view_file_multi_upload(
        files: List[UploadFile] = File(...)
):
    ctr_file = CtrFileUtils()
    res = await ctr_file.upload_multi_files(files)
    return ResponseData[List[FileBDSServiceRes]](**res)


@router.get(
    path="/multi-download/",
    description="Download multi file",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=ResponseData[List[FileDBSServiceDownloadRes]],
        success_description=status.HTTP_200_OK
    )
)
async def view_download_multi_file(uuids: List[str] = Query([])):
    ctr_file = CtrFileUtils()
    res = await ctr_file.ctr_download_multi_files(uuids)
    return ResponseData[List[FileDBSServiceDownloadRes]](**res)


@router.post(
    path="/exist/",
    description="Check file exist",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=ResponseData[List[CheckFileRes]],
        success_description=status.HTTP_200_OK
    )
)
async def view_check_file(data: List[str] = Body(..., description="list uuid")):
    ctr_file = CtrFileUtils()
    res = await ctr_file.ctr_check_files_exists(uuids=data)
    return ResponseData[List[CheckFileRes]](**res)


@router.get(
    path="/required-upload-file/",
    description="Get required upload file",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=ResponseData[Any],
        success_description=status.HTTP_200_OK
    )
)
async def view_required_upload_file():
    ctr_file = CtrFileUtils()
    res = await ctr_file.get_required_upload_file()
    return ResponseData[Any](**res)
