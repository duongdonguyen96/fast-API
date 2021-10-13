from typing import Any, Dict, List, Optional, Tuple, Union

from app.third_party.services.file import ServiceFile


async def repos_upload_file(file: bytes) -> Tuple[bool, Union[Dict, str]]:
    sv_file = ServiceFile()
    return await sv_file.upload_file(file=file)


async def repos_upload_files(files: List[bytes]) -> Tuple[bool, Union[Any, str]]:
    sv_file = ServiceFile()
    return await sv_file.upload_files(files=files)


async def repos_download_files(uuids: List[str]) -> Tuple[bool, Union[Dict, str]]:
    sv_file = ServiceFile()
    return await sv_file.download_multi_file(uuids)


async def repos_check_exist_file(uuid: str) -> Tuple[bool, Any]:
    sv_file = ServiceFile()
    is_success, res = await sv_file.check_files(uuids=[uuid])
    if not is_success:
        return False, res
    _, is_exists = res[0]
    return True, is_exists


async def repos_check_exist_files(uuids: List[str]) -> Tuple[bool, Optional[List[Tuple[str, bool]]]]:
    sv_file = ServiceFile()
    is_success, res = await sv_file.check_files(uuids=uuids)
    if not is_success:
        return False, res
    return True, res


async def repos_required_upload_file():
    sv_file = ServiceFile()
    return await sv_file.get_required_upload_file()
