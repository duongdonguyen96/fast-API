from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.card import (
    CardIssuanceType, CardType
)


class CtrDebitCard(BaseController):
    async def ctr_card_issuance_type_info(self):
        card_issuance_type_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=CardIssuanceType
            )
        )
        return self.response(card_issuance_type_info)

    async def ctr_card_type_info(self):
        card_type_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=CardType
            )
        )
        return self.response(card_type_info)
