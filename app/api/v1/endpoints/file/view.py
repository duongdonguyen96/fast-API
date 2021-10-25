from typing import List

from fastapi import APIRouter, File, Query, UploadFile
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.endpoints.file.controller import CtrFile
from app.api.v1.endpoints.file.schema import (
    FileServiceDownloadFileResponse, FileServiceResponse
)

router = APIRouter()


@router.post(
    path="/",
    name="Upload file",
    description="Upload một file",
    responses=swagger_response(
        response_model=ResponseData[FileServiceResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_file_upload(file: UploadFile = File(...)):
    file_response = await CtrFile().upload_file(file)
    return ResponseData[FileServiceResponse](**file_response)


@router.post(
    path="/multi-upload/",
    name="Upload multi-file",
    description="Upload nhiều file. "
                "Lưu ý: `Thứ tự trả về có thể không giống thứ tự gửi lên -> Cần tự check thứ tự theo tên file`",
    responses=swagger_response(
        response_model=ResponseData[List[FileServiceResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_file_multi_upload(
        file: List[UploadFile] = File(...)
):
    res = await CtrFile().upload_multi_file(file)
    return ResponseData[List[FileServiceResponse]](**res)


@router.get(
    path="/{uuid}/download/",
    name="Get link download file",
    description="Lấy link tải của một file",
    responses=swagger_response(
        response_model=ResponseData[FileServiceDownloadFileResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_download_file(uuid: str = Query(...)):
    res = await CtrFile().download_file(uuid)
    return ResponseData[FileServiceDownloadFileResponse](**res)


@router.get(
    path="/download/",
    name="Get link download multi-file",
    description="Lấy link tải của nhiều file",
    responses=swagger_response(
        response_model=ResponseData[List[FileServiceDownloadFileResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_download_multi_file(uuid: List[str] = Query([])):
    res = await CtrFile().download_multi_file(uuid)
    return ResponseData[List[FileServiceDownloadFileResponse]](**res)
