from app.api.base.controller import BaseController
from app.api.v1.endpoints.customer_service.repository import repos_get_list_kss
from app.api.v1.endpoints.customer_service.schema import QueryParamsKSSRequest


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

    async def ctr_statistics(self, months: str):
        statistics_months = [
            {
                "month": "2022-01-01T00:00:00+07:00",
                "total": 46,
                "success": 14,
                "refuse": 32
            },
            {
                "month": "2022-02-01T00:00:00+07:00",
                "total": 95,
                "success": 30,
                "refuse": 64
            }
        ]
        return self.response(statistics_months)
