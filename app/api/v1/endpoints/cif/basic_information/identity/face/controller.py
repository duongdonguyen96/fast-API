from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.face.repository import (
    repos_get_list_face
)


class CtrFace(BaseController):
    async def ctr_get_list_face(self, cif_id: str):
        face_data = self.call_repos(await repos_get_list_face(cif_id))
        return self.response(data=face_data)
