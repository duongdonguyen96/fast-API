from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.fatca.repository import (
    repos_get_fatca_data, repos_save_fatca_document
)
from app.api.v1.endpoints.cif.basic_information.fatca.schema import (
    FatcaRequest
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.third_parties.oracle.models.master_data.others import FatcaCategory
from app.utils.functions import generate_uuid, now


class CtrFatca(BaseController):
    async def ctr_save_fatca(self, cif_id: str, fatca_request: FatcaRequest):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        # lấy list fatca_category_id trong fatca_information
        fatca_category_ids = []
        for fatca_id in fatca_request.fatca_information:
            fatca_category_ids.append(fatca_id.id)

        # lấy list fatca_category_id trong document_information
        in_document_fatca_category_ids = []
        for document in fatca_request.document_information:
            for fatca_document in document.documents:
                in_document_fatca_category_ids.append(fatca_document.id)

        # RULE: Nếu Fatca info chọn có thì phải có document gửi lên
        for fatca in fatca_request.fatca_information:
            if fatca.select_flag and fatca.id not in in_document_fatca_category_ids:
                return self.response_exception(msg='', detail='fatca_information select_flag true if not document')

        fatca_category_ids.extend(in_document_fatca_category_ids)

        # check list id fatca_category có tồn tại hay không
        await self.get_model_objects_by_ids(
            model_ids=fatca_category_ids,
            model=FatcaCategory,
            loc='list_fatca_id'
        )

        fatca_category__customer_fatca_ids = {}
        for fatca in fatca_request.fatca_information:
            fatca_category__customer_fatca_ids[fatca.id] = generate_uuid()

        # lấy list data insert customer_fatca
        list_data_insert_fatca = [{
            "id": fatca_category__customer_fatca_ids[fatca.id],
            "fatca_category_id": fatca.id,
            "value": fatca.select_flag,
            "customer_id": cif_id
        } for fatca in fatca_request.fatca_information]

        # Tạp danh sách data insert fatca_document
        list_data_insert_fatca_document = []
        for language_document in fatca_request.document_information:
            for fatca_document in language_document.documents:
                list_data_insert_fatca_document.append({
                    "customer_fatca_id": fatca_category__customer_fatca_ids[fatca_document.id],
                    "document_language_type": language_document.language_type.id,
                    "document_name": 'document_name',
                    "document_url": fatca_document.url,
                    "document_version": '1',
                    "active_flag": 1,
                    'created_at': now(),
                    'order_no': None
                })

        data_response_success = self.call_repos(
            await repos_save_fatca_document(
                cif_id=cif_id,
                list_data_insert_fatca=list_data_insert_fatca,
                list_data_insert_fatca_document=list_data_insert_fatca_document,
                session=self.oracle_session,
            )
        )

        return self.response(data=data_response_success)

    async def ctr_get_fatca(self, cif_id: str):
        fatca_data = self.call_repos(await repos_get_fatca_data(cif_id=cif_id, session=self.oracle_session))

        return self.response(data=fatca_data)
