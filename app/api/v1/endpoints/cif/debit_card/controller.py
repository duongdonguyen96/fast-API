from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.debit_card.repository import (
    repos_add_debit_card, repos_debit_card
)
from app.api.v1.endpoints.cif.debit_card.schema import DebitCardRequest


class CtrDebitCard(BaseController):
    async def ctr_debit_card(self, cif_id: str):
        debit_card = self.call_repos(await repos_debit_card(cif_id))
        return self.response(debit_card)

    async def ctr_add_debit_card(self, cif_id: str, debt_card_req: DebitCardRequest):
        add_debit_card = self.call_repos(await repos_add_debit_card(cif_id, debt_card_req))
        return self.response(add_debit_card)
