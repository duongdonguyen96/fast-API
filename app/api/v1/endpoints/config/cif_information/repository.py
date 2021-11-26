from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.customer import (
    CustomerClassification, CustomerEconomicProfession
)
from app.third_parties.oracle.models.master_data.others import KYCLevel


async def repos_get_customer_classification(session: Session) -> ReposReturn:

    customer_classifications = session.execute(select(CustomerClassification)).scalars().all()
    if not customer_classifications:
        return ReposReturn(is_error=True, msg="customer_classification doesn't have data", loc='config')
    list_return_customer_classification_config = []
    for customer_classification in customer_classifications:
        list_return_customer_classification_config.append({
            "id": customer_classification.id,
            "code": customer_classification.code,
            "name": customer_classification.name
        })

    return ReposReturn(data=list_return_customer_classification_config)


async def repos_get_customer_economic_profession(session: Session) -> ReposReturn:
    customer_economic_professions = session.execute(select(CustomerEconomicProfession)).scalars().all()
    if not customer_economic_professions:
        return ReposReturn(is_error=True, msg="cust_economic_professions doesn't have data", loc='config')
    list_return_customer_economic_profession_config = []
    for customer_economic_profession in customer_economic_professions:
        list_return_customer_economic_profession_config.append({
            "id": customer_economic_profession.id,
            "code": customer_economic_profession.code,
            "name": customer_economic_profession.name
        })

    return ReposReturn(data=list_return_customer_economic_profession_config)


async def repos_get_kyc_level(session: Session) -> ReposReturn:
    kyc_levels = session.execute(select(KYCLevel)).scalars().all()
    if not kyc_levels:
        return ReposReturn(is_error=True, msg="KYC_level doesn't have data", loc='config')
    list_return_kyc_level_config = []
    for customer_economic_profession in kyc_levels:
        list_return_kyc_level_config.append({
            "id": customer_economic_profession.id,
            "code": customer_economic_profession.code,
            "name": customer_economic_profession.name
        })

    return ReposReturn(data=list_return_kyc_level_config)
