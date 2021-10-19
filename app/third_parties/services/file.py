import asyncio
from datetime import datetime
from typing import Any, Dict, List, Tuple, Union
from urllib.parse import urlparse

import aiohttp
from loguru import logger
from starlette import status

from app.settings.service import SERVICE
from app.utils.error_messages import SERVICE_ERROR


class ServiceFile:
    __host = SERVICE["file"]['url']
    __header = {
        "server-auth": SERVICE["file"]['server-auth'],
        "AUTHORIZATION": SERVICE["file"]['authorization']
    }
    __type_date_format = SERVICE["file"]['datetime-format']

    async def upload_file(self, file: bytes) -> Tuple[bool, Union[Dict, str]]:
        """
        upload 1 file to server
        """

        path = "/api/v1/files"
        method = 'POST'
        url = f'{self.__host}{path}'

        try:
            async with aiohttp.ClientSession() as session:

                res = await self.__call_upload_file(
                    session=session,
                    method=method,
                    url=url,
                    headers=self.__header,
                    file=file
                )
                if not res:
                    return False, SERVICE_ERROR

                # format datetime
                await self.__format_datetime(res)
                return True, res
        except Exception:  # noqa
            return False, SERVICE_ERROR

    async def upload_files(self, files: List[bytes]) -> Tuple[bool, Union[Any, str]]:
        """
        Upload nhiều file cùng lúc lên server
        """

        path = "/api/v1/files"
        method = 'POST'
        url = f'{self.__host}{path}'

        coroutines = list()
        try:
            async with aiohttp.ClientSession() as session:
                for file in files:
                    coroutines.append(
                        self.__call_upload_file(
                            session=session,
                            method=method,
                            url=url,
                            headers=self.__header,
                            file=file
                        )
                    )
                responses_raw = await asyncio.gather(*coroutines)

                responses = list()
                for res in responses_raw:
                    if not res:
                        return False, SERVICE_ERROR
                    # format datetime
                    await self.__format_datetime(res=res)  # noqa

                    responses.append(res)
                return True, responses
        except Exception as ex:
            logger.exception(ex)
            return False, SERVICE_ERROR

    async def download_multi_file(self, uuids: List[str]) -> Tuple[bool, Any]:
        """
        Download nhieu file cung luc
        """
        path = "/api/v1/files/download"
        method = "GET"
        url = f"{self.__host}{path}"
        try:
            async with aiohttp.ClientSession() as session:
                response_raw = await self.__call_download_files(
                    session=session,
                    method=method,
                    url=url,
                    headers=self.__header,
                    uuids=uuids
                )
                for res in response_raw:
                    data_parse_url = urlparse(res['file_url'])
                    new_data_parse_url = data_parse_url._replace(netloc='', scheme='')
                    res['file_url'] = f"/cdn{new_data_parse_url.geturl()}"

                return True, response_raw
        except Exception as ex:
            logger.exception(ex)
            return False, SERVICE_ERROR

    async def check_files(self, uuids: List[str]) -> Tuple[bool, Union[List, str]]:  # noqa
        """
        Kiểm tra file có tồn tại trên service file
        """
        path = "/api/v1/files/exist"
        method = "GET"
        url = f'{self.__host}{path}'
        coroutines = list()
        try:
            async with aiohttp.ClientSession() as session:
                for uuid in uuids:
                    coroutines.append(
                        self.__call_check_files(
                            session=session,
                            method=method,
                            url=url,
                            headers=self.__header,
                            uuids=[uuid]
                        )
                    )
                response_raw = await asyncio.gather(*coroutines)
                responses = list()
                for index, res in enumerate(response_raw):
                    responses.append((uuids[index], res,))
                return True, responses

        except Exception as ex:
            logger.exception(ex)
            return False, SERVICE_ERROR

    async def __format_datetime(self, res):
        # format datetime
        res.update({
            "created_at": datetime.strptime(
                res["created_at"],
                self.__type_date_format
            ),
            "updated_at": datetime.strptime(
                res["updated_at"],
                self.__type_date_format
            )
        })

    @staticmethod
    async def __call_upload_file(session, method, url,
                                 headers, file: bytes) -> Union[bool, Dict]:
        file_data = {
            "file": file
        }
        async with session.request(method=method, url=url, data=file_data, headers=headers) as res:
            logger.log("SERVICE", f"{res.status} : {url}")
            if res.status != status.HTTP_201_CREATED:
                return False
            return await res.json()

    @staticmethod
    async def __call_download_files(session, method, url, headers, uuids) -> Union[bool, Any]:
        params = {
            "uuid": uuids
        }
        async with session.request(method=method, url=url, headers=headers, params=params) as res:
            if res.status != status.HTTP_200_OK:
                return False
            return await res.json()

    @staticmethod
    async def __call_check_files(session, method, url, headers, uuids):
        params = {
            "uuid": uuids
        }
        async with session.request(method=method, url=url, headers=headers, params=params) as res:
            if res.status == status.HTTP_200_OK:
                return True
            return False

    @staticmethod
    async def get_required_upload_file():
        return SERVICE["file-upload"]
