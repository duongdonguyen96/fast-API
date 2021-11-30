from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.fatca.repository import (
    repos_get_fatca_data, repos_save_fatca_document
)
from app.api.v1.endpoints.cif.basic_information.fatca.schema import (
    FatcaRequest
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.third_parties.oracle.models.master_data.others import FatcaCategory
from app.utils.constant.cif import (
    ACTIVE_FLAG, LANGUAGE_ID_VN, LANGUAGE_TYPE_EN, LANGUAGE_TYPE_VN
)
from app.utils.functions import generate_uuid, now


class CtrFatca(BaseController):
    async def ctr_save_fatca(self, cif_id: str, fatca_request: FatcaRequest):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        # lấy list fatca_category_id request
        fatca_category_ids = []
        for fatca_id in fatca_request.fatca_information:
            fatca_category_ids.append(fatca_id.id)

        # lấy list fatca_document
        list_fatca_document = []
        for document in fatca_request.document_information:
            list_fatca_document.extend(document.documents)

        # lấy list fatca_document_id request
        list_fatca_document_ids = []
        for fatca_document in list_fatca_document:
            list_fatca_document_ids.append(fatca_document.id)

        # rule check document
        for fatca in fatca_request.fatca_information:
            if fatca.select_flag is True and fatca.id not in list_fatca_document_ids:
                return self.response_exception(msg='', detail='fatca_information select_flag true if not document')

        # tạo list fatca_category
        list_fatca_id = []
        list_fatca_id.extend(list_fatca_document_ids)
        list_fatca_id.extend(fatca_category_ids)

        # check list id fatca_category có tồn tại hay không
        await self.get_model_objects_by_ids(
            model_ids=list_fatca_id,
            model=FatcaCategory,
            loc='list_fatca_id')

        # lấy list data insert customer_fatca
        list_data_insert_fatca = [{
            "id": generate_uuid(),
            "fatca_category_id": fatca.id,
            "value": fatca.select_flag,
            "customer_id": cif_id
        } for fatca in fatca_request.fatca_information]

        # tạo list danh sách document
        list_document = []
        for item in fatca_request.document_information:
            for document in item.documents:
                list_document.append({
                    'id_category': document.id,
                    'language': LANGUAGE_TYPE_VN if item.language_type.id == LANGUAGE_ID_VN else LANGUAGE_TYPE_EN,
                    'url': document.url,
                })

        # Tạp danh sách data insert fatca_document
        # TODO : 1 số filed đang hash cứng dữ liệu
        list_data_insert_fatca_document = []
        for document in list_document:
            for fatca_customer in list_data_insert_fatca:
                if document['id_category'] == fatca_customer['fatca_category_id']:
                    list_data_insert_fatca_document.append({
                        "customer_fatca_id": fatca_customer['id'],
                        "document_language_type": document['language'],
                        "document_name": 'document_name',
                        "document_url": document['url'],
                        "document_version": '1',
                        "active_flag": ACTIVE_FLAG,
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
        fatca_data = self.call_repos(await repos_get_fatca_data(cif_id))

        return self.response(data=fatca_data)
