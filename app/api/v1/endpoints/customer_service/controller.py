from app.api.base.controller import BaseController
from app.api.v1.endpoints.customer_service.repository import (
    repos_create_post_check, repos_get_customer_detail,
    repos_get_history_post_post_check, repos_get_list_branch,
    repos_get_list_kss, repos_get_list_zone, repos_get_post_control,
    repos_get_statistics, repos_get_statistics_month,
    repos_get_statistics_profiles, repos_update_post_check
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
        } for branch in list_branch]

        return self.response(data=branchs)

    async def ctr_get_list_zone(self):
        list_zone = self.call_repos(await repos_get_list_zone())

        return self.response(data=list_zone)

    async def ctr_get_post_control(self, postcheck_uuid: str):
        post_control_response = self.call_repos(await repos_get_post_control(postcheck_uuid=postcheck_uuid))

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

    async def ctr_get_statistics(self, search_type: int, selected_date: str):
        query_param = {}

        query_param.update({'search_type': search_type}) if search_type else None
        query_param.update({'selected_date': selected_date}) if selected_date else None

        statistics = self.call_repos(await repos_get_statistics(query_param=query_param))

        return self.response(data=statistics)

    async def ctr_create_post_check(self, post_check_request: CreatePostCheckRequest):
        post_control_request = [{
            "check_list_id": post_control.check_list_id,
            "check_list_desc": post_control.check_list_desc,
            "answer": post_control.answer,
            "note": post_control.note
        } for post_control in post_check_request.post_control]

        payload_data = {
            "customer_id": post_check_request.customer_id,
            "kss_status": post_check_request.kss_status,
            "username": post_check_request.username,
            "post_control": post_control_request
        }

        post_check_response = self.call_repos(await repos_create_post_check(payload_data=payload_data))

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
