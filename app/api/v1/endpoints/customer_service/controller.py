from app.api.base.controller import BaseController
from app.api.v1.endpoints.customer_service.repository import (
    repos_get_customer_detail, repos_get_history_post_post_check,
    repos_get_list_branch, repos_get_list_kss, repos_get_list_zone,
    repos_get_statistics_month, repos_get_statistics_profiles,
    repos_update_post_check
)
from app.api.v1.endpoints.customer_service.schema import (
    CreatePostCheckRequest, QueryParamsKSSRequest, UpdatePostCheckRequest
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

    async def ctr_get_list_branch(self, zone_id: int):
        query_param = {
            'zone_id': zone_id
        } if zone_id else None

        list_branch = self.call_repos(await repos_get_list_branch(query_param=query_param))

        branchs = [{
            'id': branch['zone_id'],
            'code': branch['code'],
            'name': branch['name']
        }for branch in list_branch]

        return self.response(data=branchs)

    async def ctr_get_list_zone(self):
        list_zone = self.call_repos(await repos_get_list_zone())

        return self.response(data=list_zone)

    async def ctr_get_post_control(self):
        # hash cứng data
        post_control_response = {
            "kss_status": "Hợp lệ",
            "status": "2",
            "approve_status": None,
            "post_control": [
                {
                    "check_list_id": 1,
                    "check_list_desc": "Tính toàn vẹn của GTĐD",
                    "answer": "PASS",
                    "note": None
                },
                {
                    "check_list_id": 2,
                    "check_list_desc": "GTĐD không có dấu hiệu giả mạo/chỉnh sửa",
                    "answer": "PASS",
                    "note": None
                },
                {
                    "check_list_id": 3,
                    "check_list_desc": "Hình ảnh chân dung",
                    "answer": "PASS",
                    "note": None
                },
                {
                    "check_list_id": 4,
                    "check_list_desc": "Thông tin OCR so với thông tin GTĐD",
                    "answer": "PASS",
                    "note": None
                },
                {
                    "check_list_id": 5,
                    "check_list_desc": "Yếu tố khác",
                    "answer": "PASS",
                    "note": None
                }
            ]
        }
        return self.response(data=post_control_response)

    async def ctr_history_post_check(self, postcheck_uuid: str):
        history_post_check = self.call_repos(await repos_get_history_post_post_check(postcheck_uuid=postcheck_uuid))

        return self.response(data=history_post_check)

    async def ctr_statistics_month(self, months: int):
        statistics_months = self.call_repos(await repos_get_statistics_month(months=months))

        return self.response(statistics_months)

    async def ctr_get_statistics_profiles(self):

        statistics_profiles = self.call_repos(await repos_get_statistics_profiles())

        return self.response(data=statistics_profiles)

    async def ctr_get_statistics(self):
        statistics = [
            {
                "time": "00:00",
                "total": 0,
                "success": 0
            },
            {
                "time": "01:00",
                "total": 0,
                "success": 0
            },
            {
                "time": "02:00",
                "total": 0,
                "success": 0
            },
            {
                "time": "03:00",
                "total": 0,
                "success": 0
            },
            {
                "time": "04:00",
                "total": 0,
                "success": 0
            },
            {
                "time": "05:00",
                "total": 0,
                "success": 0
            },
            {
                "time": "06:00",
                "total": 0,
                "success": 0
            },
            {
                "time": "07:00",
                "total": 0,
                "success": 0
            },
            {
                "time": "08:00",
                "total": 0,
                "success": 0
            }
        ]
        return self.response(data=statistics)

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

    async def ctr_update_post_check(self, postcheck_update_request: UpdatePostCheckRequest):
        request_data = {
            "customer_id": postcheck_update_request.customer_id,
            "history_post_control_id": postcheck_update_request.history_post_control_id,
            "username": postcheck_update_request.username,
            "is_approve": postcheck_update_request.is_approve
        }
        update_post_check = self.call_repos(await repos_update_post_check(request_data=request_data))

        return self.response(data=update_post_check)

    async def ctr_get_customer_detail(self, postcheck_uuid: str):

        customer_detail = self.call_repos(await repos_get_customer_detail(postcheck_uuid=postcheck_uuid))

        return self.response(data=customer_detail)
