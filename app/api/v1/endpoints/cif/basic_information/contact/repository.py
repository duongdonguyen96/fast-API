from sqlalchemy import and_, select, update
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.basic_information.contact.model import (
    CustomerAddress, CustomerProfessional
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.utils.constant.cif import (
    CIF_ID_TEST, CONTACT_ADDRESS_CODE, RESIDENT_ADDRESS_CODE
)
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST

DOMESTIC_CONTACT_INFORMATION_DETAIL = {
    "resident_address": {
        "domestic_flag": True,
        "domestic_address": {
            "country": {
                "id": "1",
                "code": "VN",
                "name": "Việt Nam"
            },
            "number_and_street": "96 Hùng Vương",
            "province": {
                "id": "1",
                "code": "CT",
                "name": "Cần Thơ"
            },
            "district": {
                "id": "1",
                "code": "PH",
                "name": "Phụng Hiệp"
            },
            "ward": {
                "id": "1",
                "code": "TL",
                "name": "Tân Long"
            }
        },
        "foreign_address": {
            "country": {
                "id": None,
                "code": None,
                "name": None
            },
            "address_1": None,
            "address_2": None,
            "province": {
                "id": None,
                "code": None,
                "name": None
            },
            "state": {
                "id": None,
                "code": None,
                "name": None
            },
            "zip_code": {
                "id": None,
                "code": None,
                "name": None
            }
        }
    },
    "contact_address": {
        "resident_address_flag": False,
        "country": {
            "id": "1",
            "code": "VN",
            "name": "Việt Nam"
        },
        "number_and_street": "927 Trần Hưng Đạo",
        "province": {
            "id": "1",
            "code": "HCM",
            "name": "Hồ Chí Minh"
        },
        "district": {
            "id": "5",
            "code": "Q5",
            "name": "Quận 5"
        },
        "ward": {
            "id": "1",
            "code": "P1",
            "name": "Phường 1"
        }
    },
    "career_information": {
        "career": {
            "id": "1",
            "code": "XD",
            "name": "Xây dựng"
        },
        "average_income_amount": {
            "id": "1",
            "code": "LT10",
            "name": ">10 triệu"
        },
        "company_name": "Công ty ABC",
        "company_phone": "0215469874",
        "company_position": {
            "id": "1",
            "code": "NV",
            "name": "Nhân viên"
        },
        "company_address": "Số 20, Hẻm 269, Lý Tự Trọng"
    }
}

FOREIGN_CONTACT_INFORMATION_DETAIL = {
    "resident_address": {
        "domestic_flag": False,
        "domestic_address": {
            "country": {
                "id": None,
                "code": None,
                "name": None
            },
            "number_and_street": None,
            "province": {
                "id": None,
                "code": None,
                "name": None
            },
            "district": {
                "id": None,
                "code": None,
                "name": None
            },
            "ward": {
                "id": None,
                "code": None,
                "name": None
            }
        },
        "foreign_address": {
            "country": {
                "id": "1",
                "code": "USA",
                "name": "The United States of America"
            },
            "address_1": "",
            "address_2": "",
            "province": {
                "id": "1",
                "code": "LA",
                "name": "Los Angeles"
            },
            "state": {
                "id": "1",
                "code": "CALI",
                "name": "California"
            },
            "zip_code": {
                "id": "1",
                "code": "90001",
                "name": "90001"
            }
        }
    },
    "contact_address": {
        "resident_address_flag": False,
        "country": {
            "id": "1",
            "code": "VN",
            "name": "Việt Nam"
        },
        "number_and_street": "927 Trần Hưng Đạo",
        "province": {
            "id": "1",
            "code": "HCM",
            "name": "Hồ Chí Minh"
        },
        "district": {
            "id": "5",
            "code": "Q5",
            "name": "Quận 5"
        },
        "ward": {
            "id": "1",
            "code": "P1",
            "name": "Phường 1"
        }
    },
    "career_information": {
        "career": {
            "id": "1",
            "code": "XD",
            "name": "Xây dựng"
        },
        "average_income_amount": {
            "id": "1",
            "code": "LT10",
            "name": ">10 triệu"
        },
        "company_name": "Công ty ABC",
        "company_phone": "0215469874",
        "company_position": {
            "id": "1",
            "code": "NV",
            "name": "Nhân viên"
        },
        "company_address": "Số 20, Hẻm 269, Lý Tự Trọng"
    }
}


async def repos_get_detail_contact_information(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=DOMESTIC_CONTACT_INFORMATION_DETAIL)


@auto_commit
async def repos_save_contact_information(
    cif_id: str,
    customer_professional_id: str,
    is_created: bool,
    resident_address,
    contact_address,
    career_information,
    session: Session
) -> ReposReturn:
    if is_created:
        session.add_all([
            CustomerAddress(**resident_address),
            CustomerAddress(**contact_address),
            CustomerProfessional(**career_information)
        ])
        # Cập nhật lại thông tin nghề nghiệp khách hàng
        session.execute(
            update(Customer).where(Customer.id == cif_id).values(customer_professional_id=customer_professional_id)
        )
    else:
        customer_professional = session.execute(
            select(CustomerProfessional)
            .join(Customer, CustomerProfessional.id == Customer.customer_professional_id)
            .filter(Customer.id == cif_id)
        ).scalars().first()

        session.execute(
            update(CustomerAddress).where(and_(
                CustomerAddress.customer_id == cif_id,
                CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE
            )).values(**resident_address)
        )

        session.execute(
            update(CustomerAddress).where(and_(
                CustomerAddress.customer_id == cif_id,
                CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE
            )).values(**contact_address)
        )

        session.execute(
            update(CustomerProfessional).where(and_(
                CustomerProfessional.id == customer_professional.id,
            )).values(**career_information)
        )

    return ReposReturn(data={
        "cif_id": cif_id
    })


########################################################################################################################
# Others
########################################################################################################################
async def repos_get_customer_addresses(cif_id: str, session: Session):
    customer_addresses = session.execute(
        select(CustomerAddress).filter(CustomerAddress.customer_id == cif_id)).all()
    return ReposReturn(data=customer_addresses)


async def repos_get_customer_professional(cif_id: str, session: Session):
    customer_professional = session.execute(
        select(CustomerProfessional).join(Customer, and_(
            Customer.customer_professional_id == CustomerProfessional.id,
            Customer.id == cif_id
        ))
    ).scalars().first()
    return ReposReturn(data=customer_professional)
