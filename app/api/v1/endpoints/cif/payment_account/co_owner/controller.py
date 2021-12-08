from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.payment_account.co_owner.repository import (
    repos_detail_co_owner, repos_get_co_owner_data, repos_save_co_owner
)
from app.api.v1.endpoints.cif.payment_account.co_owner.schema import (
    AccountHolderRequest
)


class CtrCoOwner(BaseController):
    async def ctr_save_co_owner(self, cif_id: str, co_owner: AccountHolderRequest):
        co_owner_data = self.call_repos(
            await repos_save_co_owner(
                cif_id,
                co_owner,
                created_by=self.current_user.full_name_vn
            )
        )

        return self.response(data=co_owner_data)

    async def ctr_co_owner(self, cif_id: str):
        co_owner_data = self.call_repos(await repos_get_co_owner_data(cif_id=cif_id, session=self.oracle_session))

        return self.response(data=co_owner_data)

    async def detail_co_owner(self, cif_id: str, cif_number_need_to_find: str):
        detail_co_owner = self.call_repos(await repos_detail_co_owner(
            cif_id=cif_id,
            cif_number_need_to_find=cif_number_need_to_find,
            session=self.oracle_session
        ))

        return self.response(data=detail_co_owner)
