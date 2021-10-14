from typing import List

from app.api.base.schema import Error


class BaseValidator:
    def __init__(self, session_mongo=None, session_oracle=None):
        self.session_mongo = session_mongo
        self.session_oracle = session_oracle
        self.errors: List[Error] = []

    def _handle_list_error(self, errors: list):
        for temp in errors:
            self.errors.append(
                Error(
                    loc=" -> ".join([str(err) for err in temp["loc"]]) if len(temp["loc"]) != 0 else None,
                    msg=f"{temp['msg']}",
                    detail=temp.detail if hasattr(temp, 'detail') else None
                )
            )

    def _handle_error(self, msg: str, loc: str = None, detail: str = ""):  # noqa
        """
        Hàm add exception để trả về
        :param msg: code exception
        :param loc: fields cần thông báo
        :param detail: Thông tin thông báo
        :return:
        """
        self.errors.append(Error(msg=msg, detail=detail, loc=loc))

    def is_success(self):
        if self.errors:
            return False
        return True
