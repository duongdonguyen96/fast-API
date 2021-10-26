import asyncio
from typing import List, Optional
from urllib.parse import urlparse

import aiohttp
from loguru import logger
from starlette import status

from app.api.base.repository import ReposReturn
from app.settings.service import SERVICE
from app.utils.error_messages import ERROR_CALL_SERVICE


class ServiceFile:
    session: Optional[aiohttp.ClientSession] = None

    url = SERVICE["file"]['url']
    headers = {
        "server-auth": SERVICE["file"]['server-auth'],
        "AUTHORIZATION": SERVICE["file"]['authorization']
    }

    def start(self):
        self.session = aiohttp.ClientSession()

    async def stop(self):
        await self.session.close()
        self.session = None

    async def __call_upload_file(self, file: bytes, name: str) -> Optional[dict]:
        api_url = f'{self.url}/api/v1/files/'

        form_data = aiohttp.FormData()
        form_data.add_field('file', value=file, filename=name)

        async with self.session.post(
                url=api_url,
                data=form_data,
                headers=self.headers
        ) as response:
            logger.log("SERVICE", f"{response.status} : {api_url}")

            if response.status != status.HTTP_201_CREATED:
                return None

            return await response.json()

    async def upload_file(self, file: bytes, name: str) -> ReposReturn:
        response = await self.__call_upload_file(file=file, name=name)
        if not response:
            return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE)

        return ReposReturn(data=response)

    async def upload_multi_file(self, files: List[bytes], names: List[str]) -> ReposReturn:
        coroutines = []
        for index, file in enumerate(files):
            # coroutines.append(self.__call_upload_file(file=file))
            coroutines.append(asyncio.ensure_future(self.__call_upload_file(file=file, name=names[index])))

        responses = await asyncio.gather(*coroutines)

        success_responses = []
        for response in responses:
            if not response:
                return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE)

            success_responses.append(response)

        return ReposReturn(data=success_responses)

    async def download_file(self, uuid: str) -> ReposReturn:
        api_url = f"{self.url}/api/v1/files/{uuid}/download/"

        async with self.session.get(url=api_url, headers=self.headers) as response:
            logger.log("SERVICE", f"{response.status} : {api_url}")

            if response.status != status.HTTP_200_OK:
                return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE)

            file_download_response_body = await response.json()

            file_download_response_body['file_url'] = self.replace_with_cdn(file_download_response_body['file_url'])

        return ReposReturn(data=file_download_response_body)

    async def download_multi_file(self, uuids: List[str]) -> ReposReturn:
        api_url = f"{self.url}/api/v1/files/download/"

        async with self.session.get(url=api_url, headers=self.headers, params={'uuid': uuids}) as response:
            logger.log("SERVICE", f"{response.status} : {api_url}")

            if response.status != status.HTTP_200_OK:
                return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE)

            multi_file_download_response_body = await response.json()

        for file_download_response_body in multi_file_download_response_body:
            file_download_response_body['file_url'] = self.replace_with_cdn(file_download_response_body['file_url'])

        return ReposReturn(data=multi_file_download_response_body)

    @staticmethod
    def replace_with_cdn(file_url: str) -> str:
        file_url_parse_result = urlparse(file_url)

        # Thay thế link tải file từ service bằng CDN config theo dự án
        return file_url.replace(f'{file_url_parse_result.scheme}://{file_url_parse_result.netloc}', '/cdn')
