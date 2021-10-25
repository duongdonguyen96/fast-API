from typing import List

from app.api.base.repository import ReposReturn
from app.settings.event import service_file


async def repos_upload_file(file: bytes) -> ReposReturn:
    return await service_file.upload_file(file=file)


async def repos_upload_multi_file(files: List[bytes]) -> ReposReturn:
    return await service_file.upload_multi_file(files=files)


async def repos_download_file(uuid: str) -> ReposReturn:
    return await service_file.download_file(uuid=uuid)


async def repos_download_multi_file(uuids: List[str]) -> ReposReturn:
    return await service_file.download_multi_file(uuids=uuids)
