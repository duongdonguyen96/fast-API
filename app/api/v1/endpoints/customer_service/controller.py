from app.api.base.controller import BaseController
from app.api.v1.endpoints.customer_service.repository import repos_get_list_kss
from app.api.v1.endpoints.customer_service.schema import (
    CreatePostCheckRequest, QueryParamsKSSRequest
)


class CtrKSS(BaseController):

    async def ctr_get_list_kss(self, query_params: QueryParamsKSSRequest):
        query_data = {}

        query_data.update({'transaction_id': query_params.transaction_id}) if query_params.transaction_id else None
        query_data.update({'tran_type_id': query_params.tran_type_id}) if query_params.tran_type_id else None
        query_data.update({'approve_status': query_params.approve_status}) if query_params.approve_status else None
        query_data.update({'branch_id': query_params.branch_id}) if query_params.branch_id else None
        query_data.update({'zone_id': query_params.zone_id}) if query_params.zone_id else None
        query_data.update({'start_date': query_params.start_date}) if query_params.start_date else None
        query_data.update({'end_date': query_params.end_date}) if query_params.end_date else None
        query_data.update({'page_num': query_params.page_num}) if query_params.page_num else None
        query_data.update({'record_per_page': query_params.record_per_page}) if query_params.record_per_page else None
        query_data.update({'step_status': query_params.step_status}) if query_params.step_status else None

        list_kss = self.call_repos(await repos_get_list_kss(query_data=query_data))

        return self.response(data=list_kss)

    async def ctr_create_post_check(self, post_check_request: CreatePostCheckRequest):
        post_check_response = {
            "customer_id": "2988999b-6152-49fa-9d16-dfa79de008d6",
            "kss_status": "2",
            "username": "abc123",
            "post_control": [
                {
                    "check_list_id": 1,
                    "check_list_desc": "Tính toàn vẹn của GTĐD",
                    "answer": "PASS",
                    "note": ""
                },
                {
                    "check_list_id": 2,
                    "check_list_desc": "GTĐD không có dâu hiệu giả mạo/chỉnh sửa",
                    "answer": "PASS",
                    "note": ""
                },
                {
                    "check_list_id": 3,
                    "check_list_desc": "Hình ảnh chân dung",
                    "answer": "PASS",
                    "note": ""
                },
                {
                    "check_list_id": 4,
                    "check_list_desc": "Thông tin OCR so với thông tin trên GTĐD",
                    "answer": "PASS",
                    "note": ""
                },
                {
                    "check_list_id": 5,
                    "check_list_desc": "Yếu tố khác",
                    "answer": "PASS",
                    "note": ""
                }
            ]
        }
        return self.response(data=post_check_response)
