from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.debit_card.repository import (
    repos_add_debit_card, repos_debit_card, repos_get_list_debit_card
)
from app.api.v1.endpoints.cif.debit_card.schema import (
    DebitCardRequest, InfoDebitCardRequest
)


class CtrDebitCard(BaseController):
    async def ctr_debit_card(self, cif_id: str):
        debit_card = self.call_repos(await repos_debit_card(cif_id))
        return self.response(debit_card)

    async def ctr_add_debit_card(self, cif_id: str, debt_card_req: DebitCardRequest):
        add_debit_card = self.call_repos(await repos_add_debit_card(cif_id, debt_card_req))
        return self.response(add_debit_card)

    async def ctr_list_debit_card_type(self, cif_id: str, info_debit_card_req: InfoDebitCardRequest):
        info_debit_card_types = self.call_repos(await repos_get_list_debit_card(cif_id, info_debit_card_req))
        return self.response(info_debit_card_types)
