from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.face.repository import (
    repos_get_list_face
)
from app.utils.functions import datetime_to_date


class CtrFace(BaseController):
    async def ctr_get_list_face(self, cif_id: str):
        faces = self.call_repos(await repos_get_list_face(cif_id, self.oracle_session))

        image_uuids = [face['image_url'] for face in faces]

        # gọi đến service file để lấy link download
        uuid__link_downloads = await self.get_link_download_multi_file(uuids=image_uuids)

        date__faces = {}
        for face in faces:
            date_str = datetime_to_date(face['maker_at'])
            if date_str not in date__faces:
                date__faces[date_str] = []

            # gán lại image_url từ uuid query được trong DB thành link download từ service file
            face['image_url'] = uuid__link_downloads[face['image_url']]

            date__faces[date_str].append(face)

        data_response = [{
            'created_date': data_str,
            'faces': faces
        } for data_str, faces in date__faces.items()]

        return self.response(data=data_response)
