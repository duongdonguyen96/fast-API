from app.api.base.controller import BaseController
from app.api.v1.endpoints.customer_service.repository import repos_get_list_kss
from app.api.v1.endpoints.customer_service.schema import (
    QueryParamsKSSRequest, UpdatePostCheckRequest
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

    async def ctr_update_post_check(self, postcheck_update_request: UpdatePostCheckRequest):
        update_post_check = {
            "customer_id": "efc22caa-928b-46ff-8fa7-79b0342635b2",
            "history_post_control_id": 0,
            "username": "abc123"
        }
        return self.response(data=update_post_check)
