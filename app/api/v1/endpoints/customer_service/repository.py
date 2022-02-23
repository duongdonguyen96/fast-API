from app.api.base.repository import ReposReturn
from app.settings.event import service_ekyc


async def repos_get_list_kss(
        query_data: dict
) -> ReposReturn:
    is_success, response = await service_ekyc.get_list_kss(query_data=query_data)

    return ReposReturn(data={
        'detail': response.get('detail'),
        'total_page': response.get('total_page'),
        'total_record': response.get('total_record'),
        'page': response.get('page')
    })
