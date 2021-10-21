from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.debit_card.repository import repos_debit_card


class CtrDebitCard(BaseController):
    async def ctr_debit_card(self, cif_id: str):
        debit_card = self.call_repos(await repos_debit_card(cif_id))
        return self.response(debit_card)
