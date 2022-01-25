from app.api.base.controller import BaseController


class CtrConfigCoOwner(BaseController):
    async def ctr_agreement_info(self):
        agreement_info = [
            {
                "id": '1',
                "title": "Nội dung 1",
                "content": "Rút tiền (tiền mặt/chuyển khoản) tại quầy; Đề nghị SCB cung ứng Séc trắng và nhận Séc trắng tại SCB; Phát hành Séc; Đóng tài khoản (bao gồm Thẻ ghi Nợ và dịch vụ Ngân hàng điện tử kết nối với tài khoản) và xử lý số dư sau khi đóng tài khoản; Xác nhận số dư tài khoản; Tạm khóa/Phong tỏa tài khoản; Đề nghị SCB phát hành Thẻ ghi Nợ kết nối với tài khoản thanh toán chung tại SCB.",
                "options": [
                    {
                        "id": '1',
                        "title": 'Phương thức 1',
                        "content": "Chữ ký của tất cả các đồng "
                    },
                    {
                        "id": '2',
                        "title": 'Phương thức 2',
                        "content": "Chữ ký của 1 trong bất kỳ các đồng chủ tài khoản"
                    },
                    {
                        "id": '3',
                        "title": "Phương thức 3",
                        "content": 'Chữ ký của các đồng chủ tài khoản sau'
                    },
                ]
            },
            {
                "id": '2',
                "title": "Nội dung 2",
                "content": "Giao dịch chấm dứt tạm khóa, chấm dứt phong tỏa tài khoản và các giao dịch phát sinh khác ngoài nội dung nêu tại Nội dung 1: Chữ ký của tất cả các đồng chủ tài khoản",
                "options": [
                    {
                        "id": '1',
                        "title": "Phương thức 1",
                        "content": 'Chữ ký của tất cả đồng sở hữu'
                    }
                ]
            }
        ]
        return self.response(agreement_info)
