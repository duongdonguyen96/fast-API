from typing import Dict, Tuple, Union
from urllib.parse import urlparse

import aiohttp
from starlette import status

from app.settings.service import SERVICE
from app.utils.error_messages import SERVICE_ERROR


class ServiceTemplate:
    template_service = SERVICE["template"]
    __host = template_service['url']
    __header = {
        "server-auth": template_service['server-auth'],  # noqa
    }

    async def fill_data(self, los_id: str) -> Tuple[bool, Union[Dict, str]]:
        """
            Fill data (template)
        """

        path = "/api/v2/van-hanh/thong-tin-cif/demo-los/"
        method = 'POST'
        url = f'{self.__host}{path}'

        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        params={
                            "los_id": los_id
                        },
                        method=method,
                        url=url,
                        headers=self.__header
                ) as res:
                    # handle response
                    if res.status != status.HTTP_200_OK:
                        return False, SERVICE_ERROR

                    data = await res.json()
                    data_parse_url = urlparse(data['file_url'])
                    new_data_parse_url = data_parse_url._replace(netloc='', scheme='')

                    data['file_url'] = f"/cdn{new_data_parse_url.geturl()}"

                    return True, data

        except Exception:  # noqa
            return False, SERVICE_ERROR

    async def get_list_metadata(self, los_id: str) -> Tuple[bool, Union[Dict, str]]:
        """
            GET LIST METADATA
        """

        path = "/api/v2/van-hanh/thong-tin-cif/demo-los/"
        method = 'GET'
        url = f'{self.__host}{path}'

        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        params={
                            "los_id": los_id
                        },
                        method=method,
                        url=url,
                        headers=self.__header,
                ) as res:
                    # handle response
                    if res.status != status.HTTP_200_OK:
                        return False, SERVICE_ERROR

                    data = await res.json()
                    return True, data['template_fields']

        except Exception:  # noqa
            return False, SERVICE_ERROR
