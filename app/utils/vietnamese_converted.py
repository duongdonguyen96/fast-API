import re

patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
}


def vietnamese_converted(text: str) -> str:
    """
    Convert from 'Tiếng Việt' into 'Tieng Viet'
    """
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        # deal with upper case
        output = re.sub(regex.upper(), replace.upper(), output)
    return output


def split_name(full_name: str) -> dict[str, str]:
    """
    Split full name into first_name, middle_name, last_name
    """
    data = full_name.split(" ")
    response = None
    if len(data) >= 3:
        response = {
            "first_name": data[0],
            "middle_name": " ".join(data[1:-1]),
            "last_name": data[-1]
        }
    elif len(data) == 2:
        response = {
            "first_name": data[0],
            "middle_name": None,
            "last_name": data[-1]
        }
    return response


def make_short_name(full_name: str):
    """
    Make full name to short name
    Example: Lê Phương Thảo => thaolp
    """
    split_data = split_name(full_name)
    middle_name = split_data['middle_name']

    if len(middle_name.split(" ")) > 1:
        middle_short_name = [middle_name[0] for middle_name in middle_name.split(" ")]
        middle_name = "".join(middle_short_name)
    else:
        middle_name = middle_name[0]

    short_name = split_data['last_name'] + split_data['first_name'][0] + middle_name
    return short_name.lower()
