from typing import List

from fastapi import UploadFile
from starlette import status

from app.api.v1.controllers.base import Controller
from app.api.v1.controllers.config.file_utils.validators import (
    file_validator, files_validator
)
from app.api.v1.repositories.config.repos_file_utils import (
    repos_check_exist_files, repos_download_files, repos_required_upload_file,
    repos_upload_file, repos_upload_files
)
from app.utils.status.message import BAD_REQUEST


class CtrFileUtils(Controller):

    async def upload_file(self, upload_file: UploadFile):
        file = upload_file.file.read()
        # Validate
        is_valid, errors = file_validator(file)
        if not is_valid:
            self.errors = errors
            return self._response(data=None, error_status_code=status.HTTP_400_BAD_REQUEST)

        # Upload file
        is_success, _file_res = await repos_upload_file(file)
        if not is_success:
            self._response_exception(msg=_file_res)
        return self._response(data=_file_res)

    async def upload_multi_files(self, upload_files: List[UploadFile]):
        files = [upload_file.file.read() for upload_file in upload_files]

        # Validate
        is_valid, errors = files_validator(files)
        if not is_valid:
            self.errors = errors
            return self._response(data=None, error_status_code=status.HTTP_400_BAD_REQUEST)

        # Upload files
        is_success, _responses = await repos_upload_files(files)
        if not is_success:
            return self._response_exception(msg=_responses)
        return self._response(data=_responses)

    async def ctr_download_multi_files(self, uuids: List[str]):
        # When there no file
        if len(uuids) < 1:
            return self._response_exception(msg=BAD_REQUEST, error_status_code=status.HTTP_400_BAD_REQUEST)

        is_sucess, res = await repos_check_exist_files(uuids)
        if not is_sucess:
            return self._response_exception(msg=res, error_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # When a file not exist
        for uuid, is_exist in res:
            if not is_exist:
                return self._response_exception(msg=f"{uuid} not exists", error_status_code=status.HTTP_400_BAD_REQUEST)

        is_success, files = await repos_download_files(uuids=uuids)
        if not is_success:
            return self._response_exception(msg=files)
        return self._response(data=files)

    async def ctr_check_files_exists(self, uuids: List[str]):
        # When there no file
        if len(uuids) < 1:
            return self._response_exception(msg=BAD_REQUEST, error_status_code=status.HTTP_400_BAD_REQUEST)
        response = list()
        is_success, res = await repos_check_exist_files(uuids=uuids)
        if not is_success:
            return self._response_exception(res)
        for uuid, is_exists in res:
            response.append({
                "uuid": uuid,
                "is_exist": is_exists
            })
        return self._response(data=response)

    async def get_required_upload_file(self):
        config = await repos_required_upload_file()
        return self._response(data=config)
