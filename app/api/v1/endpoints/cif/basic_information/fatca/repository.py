from app.api.base.repository import ReposReturn
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST


async def repos_get_fatca_data(cif_id: str):
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "fatca_information": [
            {
                "id": "1",
                "code": "code",
                "name": "Quý khác là công dân Hoa Kỳ hoặc thường trú hợp pháp tại Hoa Kỳ(có thẻ xanh)",
                "active_flag": True
            },
            {
                "id": "2",
                "code": "code",
                "name": "Quý khách có sinh ra tại Hoa Kỳ không",
                "active_flag": False
            },
            {
                "id": "3",
                "code": "code",
                "name": "Quý khách có thư ủy quyền hoặc ủy quyền cho "
                        "một cá nhân/tổ chức có địa chỉ tại Hoa Kỳ không",
                "active_flag": True
            },
            {
                "id": "4",
                "code": "code",
                "name": "Quý khách có lệnh chuyển tiền tới tài khoản tại Hoa Kỳ "
                        "hoặc khoản tiền nhận được thường xuyên từ một địa chỉ Hoa Kỳ không",
                "active_flag": True
            },
            {
                "id": "5",
                "code": "code",
                "name": "Quý khách có địa chỉ thư tín (bao gồm hộp thư bưu điện)"
                        " hoặc nơi cư trú hiện tại ở Hoa Kỳ hoặc số điện thoại Hoa Kỳ",
                "active_flag": True
            },
            {
                "id": "6",
                "code": "code",
                "name": "Quý khách có địa chỉ “nhờ chuyển thư” hoặc “giữ thư” tại Hoa Kỳ",
                "active_flag": False
            }
        ],
        "documents_list": [
            {
                "language_type": {
                    "id": "1",
                    "code": "VN",
                    "name": "vn"
                },
                "documents": [
                    {
                        "id": "1",
                        "name": "W-8BEN",
                        "url": "url-w8ben",
                        "active_flag": True,
                        "version": "1.0",
                        "content_type": "Word",
                        "size": "1MB",
                        "folder": "Khởi tạo CIF",
                        "created_by": "Nguyễn Phúc",
                        "created_at": "2020-12-29 06:07:08",
                        "updated_by": "Trần Bình Liên",
                        "updated_at": "2020-12-30 06:07:08",
                        "note": "Tài liệu quan trọng"
                    },
                    {
                        "id": "2",
                        "name": "W-8BEN",
                        "url": "url-w8ben",
                        "active_flag": True,
                        "version": "1.0",
                        "content_type": "Word",
                        "size": "1MB",
                        "folder": "Khởi tạo CIF",
                        "created_by": "Nguyễn Phúc",
                        "created_at": "2020-12-28 06:07:08",
                        "updated_by": "Trần Bình Liên",
                        "updated_at": "2020-12-29 06:07:08",
                        "note": "Tài liệu quan trọng"
                    }
                ]
            },
            {
                "language_type": {
                    "id": "2",
                    "code": "EN",
                    "name": "en"
                },
                "documents": [
                    {
                        "id": "3",
                        "name": "W-8BEN",
                        "url": "url-w8ben",
                        "active_flag": True,
                        "version": "1.0",
                        "content_type": "Word",
                        "size": "1MB",
                        "folder": "Khởi tạo CIF",
                        "created_by": "Nguyễn Phúc",
                        "created_at": "2020-12-27 06:07:08",
                        "updated_by": "Trần Bình Liên",
                        "updated_at": "2020-12-28 06:07:08",
                        "note": "import document"
                    },
                    {
                        "id": "4",
                        "name": "W-8BEN",
                        "url": "url-w8ben",
                        "active_flag": True,
                        "version": "1.0",
                        "content_type": "Word",
                        "size": "1MB",
                        "folder": "Khởi tạo CIF",
                        "created_by": "Nguyễn Phúc",
                        "created_at": "2020-12-26 06:07:08",
                        "updated_by": "Trần Bình Liên",
                        "updated_at": "2020-12-27 06:07:08",
                        "note": "import document"
                    }
                ]
            }
        ]
    })
