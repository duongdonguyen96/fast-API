from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.hand.repository import (
    repos_get_finger_printer, repos_get_hand_side
)


class CtrConfigHand(BaseController):
    async def ctr_hand_side_info(self):
        hand_side_info = self.call_repos(await repos_get_hand_side(self.oracle_session))
        return self.response(hand_side_info)

    async def ctrl_finger_printer(self):
        finger_printer_info = self.call_repos(await repos_get_finger_printer(self.oracle_session))
        return self.response(finger_printer_info)
