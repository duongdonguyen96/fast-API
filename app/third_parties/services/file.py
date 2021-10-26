import asyncio
from typing import List, Optional
from urllib.parse import urlparse

import aiohttp
from loguru import logger
from starlette import status

from app.settings.service import SERVICE


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
            logger.log("SERVICE FILE", f"{response.status} : {api_url}")

            if response.status != status.HTTP_201_CREATED:
                return None

            return await response.json()

    async def upload_file(self, file: bytes, name: str) -> Optional[dict]:
        return await self.__call_upload_file(file=file, name=name)

    async def upload_multi_file(self, files: List[bytes], names: List[str]) -> Optional[List[dict]]:
        coroutines = []
        for index, file in enumerate(files):
            # coroutines.append(self.__call_upload_file(file=file))
            coroutines.append(asyncio.ensure_future(self.__call_upload_file(file=file, name=names[index])))

        return list(await asyncio.gather(*coroutines))

    async def download_file(self, uuid: str) -> Optional[dict]:
        api_url = f"{self.url}/api/v1/files/{uuid}/download/"

        async with self.session.get(url=api_url, headers=self.headers) as response:
            logger.log("SERVICE FILE", f"{response.status} : {api_url}")

            if response.status != status.HTTP_200_OK:
                return None

            file_download_response_body = await response.json()

            file_download_response_body['file_url'] = self.replace_with_cdn(file_download_response_body['file_url'])

        return file_download_response_body

    async def download_multi_file(self, uuids: List[str]) -> Optional[List[dict]]:
        api_url = f"{self.url}/api/v1/files/download/"

        async with self.session.get(url=api_url, headers=self.headers, params={'uuid': uuids}) as response:
            logger.log("SERVICE FILE", f"{response.status} : {api_url}")

            if response.status != status.HTTP_200_OK:
                return None

            multi_file_download_response_body = await response.json()

        for file_download_response_body in multi_file_download_response_body:
            file_download_response_body['file_url'] = self.replace_with_cdn(file_download_response_body['file_url'])

        return multi_file_download_response_body

    @staticmethod
    def replace_with_cdn(file_url: str) -> str:
        file_url_parse_result = urlparse(file_url)

        # Thay thế link tải file từ service bằng CDN config theo dự án
        return file_url.replace(f'{file_url_parse_result.scheme}://{file_url_parse_result.netloc}', '/cdn')
