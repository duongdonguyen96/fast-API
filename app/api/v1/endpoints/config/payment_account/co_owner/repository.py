from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.payment_account.model import (
    AgreementAuthorization
)


async def repos_get_agreement_authorization(session: Session):
    account_structure_type_infos = session.execute(
        select(
            AgreementAuthorization
        )
        .filter(AgreementAuthorization.agreement_author_type == "FD")  # TODO
    ).scalars().all()

    return ReposReturn(data=[{
        "id": account_structure_type_info.id,
        "content": account_structure_type_info.name,
        "options": [  # TODO
            {
                "id": '1',
                "title": 'Phương thức 1',
                "content": "Chữ ký của tất cả các đồng sở hữu"
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
    } for account_structure_type_info in account_structure_type_infos])
