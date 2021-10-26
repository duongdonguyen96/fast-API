from typing import Optional, Tuple

import aiohttp
from loguru import logger
from starlette import status

from app.settings.service import SERVICE


class ServiceCard:
    session: Optional[aiohttp.ClientSession] = None

    url = SERVICE["card"]["url"]
    headers = {
        "AUTHORIZATION": SERVICE["card"]["authorization"],
        "X-TRANSACTION-ID": SERVICE["card"]["x-transaction-id"]
    }

    def start(self):
        self.session = aiohttp.ClientSession()

    async def stop(self):
        await self.session.close()
        self.session = None

    async def ocr_identity_document(self, file: bytes, filename: str, document_type: int) -> Tuple[bool, dict]:
        api_url = f"{self.url}/api/v1/card-service/ocr/"

        form_data = aiohttp.FormData()
        form_data.add_field("file", value=file, filename=filename)
        form_data.add_field("type", value=str(document_type))

        is_error = False

        async with self.session.post(url=api_url, data=form_data, headers=self.headers) as response:
            logger.log("SERVICE", f"[CARD] {response.status} : {api_url}")

            if response.status != status.HTTP_200_OK:
                is_error = True

            response_body = await response.json()

        return is_error, response_body
