from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.fatca.repository import (
    repos_get_fatca_category_ids, repos_get_fatca_customer,
    repos_get_fatca_data, repos_save_fatca, repos_save_fatca_document
)
from app.api.v1.endpoints.cif.basic_information.fatca.schema import (
    FatcaRequest
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.utils.constant.cif import (
    LANGUAGE_ID_EN, LANGUAGE_ID_VN, LANGUAGE_TYPE_EN, LANGUAGE_TYPE_VN
)
from app.utils.functions import now


class CtrFatca(BaseController):
    async def ctr_save_fatca(self, cif_id: str, fatca: FatcaRequest):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        # lấy list id fatca_category request
        fatca_category_ids = []
        for fatca_id in fatca.fatca_information:
            fatca_category_ids.append(fatca_id.id)

        # fatca_category_ids = list(set(fatca_category_ids))
        # check list id fatca_category có tồn tại hay không
        self.call_repos(
            await repos_get_fatca_category_ids(fatca_category_ids=fatca_category_ids, session=self.oracle_session))

        # lấy list data insert customer_fatca
        list_data_insert_fatca = [{
            "fatca_category_id": fatca.id,
            "value": fatca.select_flag,
            "customer_id": cif_id
        } for fatca in fatca.fatca_information]

        # lưu customer_fatca vào bảng crm_customer_fatca
        self.call_repos(
            await repos_save_fatca(
                list_data_insert_fatca=list_data_insert_fatca,
                session=self.oracle_session
            )
        )

        # tạo list danh sách document
        list_document = []
        for item in fatca.documents_information:
            if item.language_type.id == LANGUAGE_ID_VN:
                for document in item.documents:
                    list_document.append({
                        'id_category': document.id,
                        'name': document.name,
                        'language': LANGUAGE_TYPE_VN,
                        'url': document.url,
                        'version': document.version,
                        'active_flag': document.active_flag
                    })
            if item.language_type.id == LANGUAGE_ID_EN:
                for document in item.documents:
                    list_document.append({
                        'id_category': document.id,
                        'language': LANGUAGE_TYPE_EN,
                        'name': document.name,
                        'url': document.url,
                        'version': document.version,
                        'active_flag': document.active_flag
                    })
        # lấy danh sách id document request
        list_document_ids = []
        for document in list_document:
            list_document_ids.append(document['id_category'])

        list_document_ids = list(set(list_document_ids))
        # check list id document in fatca_category
        self.call_repos(
            await repos_get_fatca_category_ids(
                fatca_category_ids=list_document_ids,
                session=self.oracle_session
            )
        )
        # lấy data customer_fatca vừa tạo fatca theo cif_id
        list_fatca_customer = self.call_repos(
            await repos_get_fatca_customer(cif_id=cif_id, session=self.oracle_session))

        # Tạp danh sách data insert fatca_document
        list_data_insert_fatca_document = []
        for document in list_document:
            for fatca_customer in list_fatca_customer:
                if document['id_category'] == fatca_customer.fatca_category_id:
                    list_data_insert_fatca_document.append({
                        "customer_fatca_id": fatca_customer.id,
                        "document_language_type": document['language'],
                        "document_name": document['name'],
                        "document_url": document['url'],
                        "document_version": document['version'],
                        "active_flag": document['active_flag'],
                        'created_at': now(),
                        'order_no': None
                    })

        data_response_success = self.call_repos(
            await repos_save_fatca_document(
                cif_id=cif_id,
                list_data_insert_fatca_document=list_data_insert_fatca_document,
                session=self.oracle_session,
                created_by=self.current_user.full_name_vn
            )
        )
        return self.response(data=data_response_success)

    async def ctr_get_fatca(self, cif_id: str):
        fatca_data = self.call_repos(await repos_get_fatca_data(cif_id))

        return self.response(data=fatca_data)
