from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.card import (
    BrandOfCard, CardIssuanceFee, CardIssuanceType, CardType
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

    async def ctr_card_fee(self):
        """
            Phí phát hành thẻ
        """
        card_issuance_fees = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=CardIssuanceFee
            )
        )
        return self.response(card_issuance_fees)

    async def ctr_brand_of_card(self):
        """
            Thương hiệu thẻ
        """
        brand_of_cards = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=BrandOfCard
            )
        )
        return self.response(brand_of_cards)
