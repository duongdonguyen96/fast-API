from typing import Optional, Tuple

import aiohttp
from loguru import logger
from starlette import status

from app.settings.service import SERVICE


class ServiceEKYC:
    session: Optional[aiohttp.ClientSession] = None

    url = SERVICE["ekyc"]['url']
    headers = {
        "X-TRANSACTION-ID": SERVICE["ekyc"]['x-transaction-id'],
        "AUTHORIZATION": SERVICE["ekyc"]['authorization']
    }

    def start(self):
        self.session = aiohttp.ClientSession()

    async def stop(self):
        await self.session.close()
        self.session = None

    async def ocr_identity_document(self, file: bytes, filename: str, identity_type: int) -> Tuple[bool, dict]:
        api_url = f"{self.url}/api/v1/card-service/ocr/"

        form_data = aiohttp.FormData()
        form_data.add_field("file", value=file, filename=filename)
        form_data.add_field("type", value=str(identity_type))

        is_success = True

        try:
            async with self.session.post(url=api_url, data=form_data, headers=self.headers) as response:
                logger.log("SERVICE", f"[CARD] {response.status} : {api_url}")

                if response.status != status.HTTP_200_OK:
                    is_success = False

                response_body = await response.json()
        except Exception as ex:
            logger.error(str(ex))
            return False, {}

        return is_success, response_body
