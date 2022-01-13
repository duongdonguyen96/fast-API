from typing import Optional

import aiohttp
from loguru import logger
from starlette import status

from app.settings.service import SERVICE
from app.utils.constant.soa import SOA_REPONSE_STATUS_SUCCESS


class ServiceSOA:
    session: Optional[aiohttp.ClientSession] = None

    url = SERVICE["soa"]['url']
    username = SERVICE["soa"]["authorization_username"]
    password = SERVICE["soa"]["authorization_password"]
    soa_basic_auth = aiohttp.BasicAuth(login=username, password=password, encoding='utf-8')

    def start(self):
        self.session = aiohttp.ClientSession(auth=self.soa_basic_auth)

    async def stop(self):
        await self.session.close()
        self.session = None

    async def retrieve_customer_ref_data_mgmt(self, cif_number: str):
        """
        Input: cif_number - Số CIF
        Output: (is_success, is_existed/error_message) - Thành công, Có tồn tại/ Lỗi Service SOA
        """
        cif_number = cif_number
        is_success = True
        request_data = {
            "retrieveCustomerRefDataMgmt_in": {
                "transactionInfo": {
                    "clientCode": "INAPPTABLET",  # TODO
                    "cRefNum": "CRM1641783511239",  # TODO
                    "branchInfo": {
                        "branchCode": "001"  # TODO
                    }
                },
                "CIFInfo": {
                    "CIFNum": cif_number
                }
            }
        }
        api_url = f"{self.url}/customerrefdatamgmt/v1.0/rest/retrieveCustomerRefDataMgmt"
        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[SOA] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    logger.error(f"[STATUS]{str(response.status)} [ERROR_INFO]")
                    return False, "Service SOA Status error please try again later"

                response_data = await response.json()
                # Nếu không tồn tại CIF
                if response_data["retrieveCustomerRefDataMgmt_out"]["transactionInfo"]["transactionReturn"] != SOA_REPONSE_STATUS_SUCCESS:
                    is_existed = False
                else:
                    is_existed = True

        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, "Connect to service SOA error please try again later"
        except KeyError as ex:
            logger.error(str(ex))
            return False, "Key error " + str(ex)

        return is_success, is_existed
