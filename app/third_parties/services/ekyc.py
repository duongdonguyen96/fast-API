from typing import Optional, Tuple

import aiohttp
from aiohttp.web_exceptions import HTTPException
from loguru import logger
from starlette import status

from app.settings.service import SERVICE


class ServiceEKYC:
    session: Optional[aiohttp.ClientSession] = None

    url = SERVICE["ekyc"]['url']
    headers = {
        "X-TRANSACTION-ID": SERVICE["ekyc"]['x-transaction-id'],
        "AUTHORIZATION": SERVICE["ekyc"]['authorization'],
        "X-DEVICE-INFO": "eyJkZXZpY2VOYW1lIjoibWluaOKAmXMgaVBob25lIiwib3MiOiJJT1MiLCJtb2RlbCI6ImlQaG9uZSBYUiIsInBob25lX"
                         "251bWJlciI6IjA5MDI0MDk2NjQiLCJtYW51ZmFjdHVyZXIiOiJBcHBsZSIsIm9zVmVyc2lvbiI6IjE0LjEifQ"  # TODO
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
            print('#######################TRUNG TEST##################')
            print(api_url)
            return False, {}

        # chỗ này fail trả về response_body để trả luôn message lỗi bên eKYC
        return is_success, response_body

    async def add_face(self, file: bytes):
        """
        Thêm 1 ảnh người vào trong eKYC
        """
        api_url = f"{self.url}/api/v1/face-service/add/"
        form_data = aiohttp.FormData()
        form_data.add_field("file", value=file, filename='abc.jpg')

        is_success = True
        try:
            async with self.session.post(url=api_url, data=form_data, headers=self.headers) as response:
                logger.log("SERVICE", f"[FACE] {response.status} : {api_url}")
                if response.status != status.HTTP_201_CREATED:
                    is_success = False
                response_body = await response.json()
        except Exception as ex:
            logger.error(str(ex))
            return False, {}

        # chỗ này fail trả về response_body để trả luôn message lỗi bên eKYC
        return is_success, response_body

    async def compare_face(self, face_uuid: str, avatar_image_uuid: str):
        """
        So sánh khuôn mặt trong 2 ảnh
        """
        api_url = f"{self.url}/api/v1/face-service/compare/"

        is_success = True
        data = {
            "image_face_1_uuid": face_uuid,
            "image_face_2_uuid": avatar_image_uuid
        }

        try:
            async with self.session.post(url=api_url, json=data, headers=self.headers) as response:
                logger.log("SERVICE", f"[FACE] {response.status} : {api_url}")

                if response.status != status.HTTP_200_OK:
                    is_success = False
                response_body = await response.json()
        except HTTPException as ex:
            logger.error(str(ex))
            return False, {"message": "eKYC server error, please try again"}

        return is_success, response_body

    async def validate(self, data, document_type):
        api_url = f"{self.url}/api/v1/card-service/validate/"

        is_success = True
        request_body = {
            "document_type": document_type,
            "data": data
        }

        try:
            async with self.session.post(url=api_url, json=request_body, headers=self.headers) as response:
                logger.log("SERVICE", f"[VALIDATE] {response.status} : {api_url}")
                if response.status != status.HTTP_200_OK:
                    is_success = False
                response_body = await response.json()
                if not response_body['success']:
                    is_success = False
        except Exception as ex:
            logger.error(str(ex))
            return False, {"errors": {"message": "eKYC error please try again later"}}

        return is_success, response_body
