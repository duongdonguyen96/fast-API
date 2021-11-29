from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.identity import (
    FingerType, HandSide
)


class CtrConfigHand(BaseController):
    async def ctr_hand_side_info(self):
        hand_side_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=HandSide
            )
        )
        return self.response(hand_side_info)

    async def ctr_finger_printer(self):
        finger_printer_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=FingerType
            )
        )
        return self.response(finger_printer_info)
