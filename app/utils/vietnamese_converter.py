import re
from typing import Optional, Tuple, Union

patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
}


def convert_to_unsigned_vietnamese(text: str) -> str:
    """
    Convert from 'Tiếng Việt' into 'Tieng Viet'
    """
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        # deal with upper case
        output = re.sub(regex.upper(), replace.upper(), output)
    return output


# TODO: sửa lại hàm này first name là tên
def split_name(full_name: str) -> Union[Tuple[str, str, str], Tuple[str, None, str], Tuple[None, None, None]]:
    """
    Split full_name into first_name, middle_name, last_name
    """
    data = full_name.split(" ")
    if len(data) >= 3:
        return data[0], " ".join(data[1:-1]), data[-1]
    elif len(data) == 2:
        return data[0], None, data[-1]
    else:
        return None, None, None


# TODO: sửa lại hàm này, middle name có thể rỗng
def make_short_name(first_name: str, middle_name: Optional[str], last_name: str):
    """
    Make full name to short name
    Example: Lê Phương Thảo => thaolp
    """
    if len(middle_name.split(" ")) > 1:
        middle_short_name = [middle_name[0] for middle_name in middle_name.split(" ")]
        middle_name = "".join(middle_short_name)
    else:
        middle_name = middle_name[0]

    short_name = last_name + first_name[0] + middle_name
    return short_name.lower()
