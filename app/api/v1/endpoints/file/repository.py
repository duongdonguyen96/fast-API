from typing import List

from app.api.base.repository import ReposReturn
from app.settings.event import service_file


async def repos_upload_file(file: bytes, name: str) -> ReposReturn:
    return await service_file.upload_file(file=file, name=name)


async def repos_upload_multi_file(files: List[bytes], names: List[str]) -> ReposReturn:
    return await service_file.upload_multi_file(files=files, names=names)


async def repos_download_file(uuid: str) -> ReposReturn:
    return await service_file.download_file(uuid=uuid)


async def repos_download_multi_file(uuids: List[str]) -> ReposReturn:
    return await service_file.download_multi_file(uuids=uuids)
