from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.debit_card.repository import (
    repos_add_debit_card, repos_debit_card, repos_get_list_debit_card
)
from app.api.v1.endpoints.cif.debit_card.schema import DebitCardRequest


class CtrDebitCard(BaseController):
    async def ctr_debit_card(self, cif_id: str):
        debit_card = self.call_repos(await repos_debit_card(cif_id))
        return self.response(debit_card)

    async def ctr_add_debit_card(self, cif_id: str, debt_card_req: DebitCardRequest):
        add_debit_card = self.call_repos(await repos_add_debit_card(cif_id, debt_card_req))
        return self.response(add_debit_card)

    async def ctr_list_debit_card_type(self, cif_id: str,
                                       branch_of_card_id: str,
                                       issuance_fee_id: str,
                                       annual_fee_id: str,
                                       ):
        info_debit_card_types = self.call_repos(
            await repos_get_list_debit_card(
                cif_id,
                branch_of_card_id,
                issuance_fee_id,
                annual_fee_id
            ))
        return self.response(info_debit_card_types)
