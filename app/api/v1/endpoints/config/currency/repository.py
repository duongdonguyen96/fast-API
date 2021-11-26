from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.others import Currency


async def repos_get_currency(session: Session) -> ReposReturn:

    currencies = session.execute(select(Currency)).scalars().all()
    if not currencies:
        return ReposReturn(is_error=True, msg="currency doesn't have data", loc='config')
    list_currency_config = []
    for currency in currencies:
        list_currency_config.append({
            "id": currency.id,
            "code": currency.code,
            "name": currency.name
        })

    return ReposReturn(data=list_currency_config)
