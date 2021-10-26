from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.form.repository import repos_approval_process


class CtrForm(BaseController):
    async def ctr_approval_process(self, cif_id: str):
        approval_process = self.call_repos((await repos_approval_process(cif_id)))
        return self.response(approval_process)
