from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.payment_account.model import CasaAccount
from app.third_parties.oracle.models.master_data.account import AccountClass, AccountType
from app.third_parties.oracle.models.master_data.others import Currency
from app.utils.functions import now, dropdown

NO_REQUIREMENT_PAYMENT_ACCOUNT_INFO_DETAIL = {
    "self_selected_account_flag": False,
    "currency": {
        "id": "1",
        "code": "VND",
        "name": "Việt Nam Đồng"
    },
    "account_type": {
        "id": "1",
        "code": "LOCPHAT",
        "name": "Lộc Phát"
    },
    "account_class": {
        "id": "1",
        "code": "LOAIHINH1",
        "name": "Loại Hình 1"
    },
    "account_structure_type_level_1": {
        "id": None,
        "code": None,
        "name": None
    },
    "account_structure_type_level_2": {
        "id": None,
        "code": None,
        "name": None
    },
    "account_structure_type_level_3": {
        "id": None,
        "code": None,
        "name": None
    },
    "casa_account_number": None,
    "account_salary_organization_account": "13245678912",
    "account_salary_organization_name": None
}


async def repos_detail_payment_account(cif_id: str, session: Session) -> ReposReturn:
    details = session.execute(
        select(
            CasaAccount,
            Currency,
            AccountClass,
            AccountType

        ).join(
            Currency,
            CasaAccount.currency_id == Currency.id)
        .join(
            AccountClass,
            CasaAccount.acc_class_id == AccountClass.id)
        .join(
            AccountType,
            CasaAccount.acc_type_id == AccountType.id)
        .filter(
            CasaAccount.customer_id == cif_id
        )
    ).first()

    return ReposReturn(data={
        "self_selected_account_flag": details.CasaAccount.self_selected_account_flag,
        "currency": dropdown(details.Currency),
        "account_type": dropdown(details.AccountType),
        "account_class": dropdown(details.AccountClass),
        "account_structure_type_level_1": {
            "id": None,
            "code": None,
            "name": None
        },
        "account_structure_type_level_2": {
            "id": None,
            "code": None,
            "name": None
        },
        "account_structure_type_level_3": {
            "id": None,
            "code": None,
            "name": None
        },
        "casa_account_number": details.CasaAccount.case_account_number,
        "account_salary_organization_account": details.CasaAccount.acc_salary_org_acc,
        "account_salary_organization_name": details.CasaAccount.acc_salary_org_name

    })


@auto_commit
async def repos_save_payment_account(
        cif_id: str,
        list_data_insert: list,
        created_by: str,
        session: Session,
):
    data_insert = [CasaAccount(**casa_acc) for casa_acc in list_data_insert]
    session.bulk_save_objects(data_insert)

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })
