from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.contact.repository import (
    repos_get_detail_contact_information, repos_save_contact_information
)
from app.api.v1.endpoints.cif.basic_information.contact.schema import (
    ContactInformationSaveRequest
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.others import (
    AverageIncomeAmount, Career, Position
)
from app.utils.constant.cif import (
    ADDRESS_COUNTRY_CODE_VN, CONTACT_ADDRESS_CODE, RESIDENT_ADDRESS_CODE
)
from app.utils.functions import check_exist_list_by_id, check_not_null


class CtrContactInformation(BaseController):
    async def detail_contact_information(self, cif_id: str):
        contact_information_detail_data = self.call_repos(
            await repos_get_detail_contact_information(cif_id=cif_id)
        )
        return self.response(data=contact_information_detail_data)

    async def save_contact_information(
            self, cif_id: str,
            contact_information_save_request: ContactInformationSaveRequest
    ):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        # Địa chỉ thường trú
        resident_address_domestic_flag = contact_information_save_request.resident_address.domestic_flag
        resident_address_domestic_address_country_id = contact_information_save_request.resident_address.domestic_address.country.id
        resident_address_domestic_address_province_id = contact_information_save_request.resident_address.domestic_address.province.id
        resident_address_domestic_address_district_id = contact_information_save_request.resident_address.domestic_address.district.id
        resident_address_domestic_address_ward_id = contact_information_save_request.resident_address.domestic_address.ward.id
        resident_address_domestic_number_and_street = contact_information_save_request.resident_address.domestic_address.number_and_street

        resident_address_foreign_address_country_id = contact_information_save_request.resident_address.foreign_address.country.id
        resident_address_foreign_address_province_id = contact_information_save_request.resident_address.foreign_address.province.id
        resident_address_foreign_address_state_id = contact_information_save_request.resident_address.foreign_address.state.id
        resident_address_foreign_address_address_1 = contact_information_save_request.resident_address.foreign_address.address_1
        resident_address_foreign_address_address_2 = contact_information_save_request.resident_address.foreign_address.address_2
        resident_address_foreign_zip_code = contact_information_save_request.resident_address.foreign_address.zip_code

        # Địa chỉ liên lạc
        contact_address_resident_address_flag = contact_information_save_request.contact_address.resident_address_flag
        contact_address_country_id = contact_information_save_request.contact_address.country.id
        contact_address_province_id = contact_information_save_request.contact_address.province.id
        contact_address_district_id = contact_information_save_request.contact_address.district.id
        contact_address_ward_id = contact_information_save_request.contact_address.ward.id
        contact_address_number_and_street = contact_information_save_request.contact_address.number_and_street

        # Thông tin nghề nghiệp
        career_id = contact_information_save_request.career_information.career.id
        average_income_amount_id = contact_information_save_request.career_information.average_income_amount.id
        company_position_id = contact_information_save_request.career_information.company_position.id
        company_name = contact_information_save_request.career_information.company_name
        company_phone = contact_information_save_request.career_information.company_phone
        company_address = contact_information_save_request.career_information.company_address

        list_exist = []
        list_not_null = []

        ################################################################################################################
        # Địa chỉ thường trú
        ################################################################################################################
        resident_address = {
            "customer_id": cif_id,
            "address_type_id": RESIDENT_ADDRESS_CODE
        }
        contact_address = {
            "customer_id": cif_id,
            "address_type_id": CONTACT_ADDRESS_CODE
        }
        # Nếu là địa chỉ trong nước
        if resident_address_domestic_flag:
            list_require = [
                (resident_address_domestic_address_country_id, AddressCountry,
                 "resident_address -> domestic_address -> country -> id"),
                (resident_address_domestic_address_province_id, AddressProvince,
                 "resident_address -> domestic_address -> province -> id"),
                (resident_address_domestic_address_district_id, AddressDistrict,
                 "resident_address -> domestic_address -> district -> id"),
                (resident_address_domestic_address_ward_id, AddressWard,
                 "resident_address -> domestic_address -> ward -> id")
            ]
            list_not_null.extend(list_require)
            list_exist.extend(list_require)

            resident_address.update({
                "address_country_id": resident_address_domestic_address_country_id,
                "address_province_id": resident_address_domestic_address_province_id,
                "address_district_id": resident_address_domestic_address_district_id,
                "address_ward_id": resident_address_domestic_address_ward_id,
                "address": resident_address_domestic_number_and_street,
                "zip_code": None,
                "latitude": None,
                "longitude": None,
                "address_primary_flag": None,
                "address_domestic_flag": resident_address_domestic_flag,
                "address_2": None,
                "address_same_permanent_flag": None
            })
            ############################################################################################################
            # Địa chỉ liên lạc
            ############################################################################################################
            # Nếu giống địa chỉ thường trú
            if contact_address_resident_address_flag:
                contact_address.update(resident_address)
                # Giống địa chỉ thường trú nhưng vẫn là tạm trú
                contact_address.update({
                    "address_same_permanent_flag": True,
                    "address_type_id": CONTACT_ADDRESS_CODE
                })
            # Nếu khác địa chỉ thường trú
            else:
                list_require.extend([
                    (contact_address_country_id, AddressCountry, "contact_address -> country -> id"),
                    (contact_address_province_id, AddressProvince, "contact_address -> province -> id"),
                    (contact_address_district_id, AddressDistrict, "contact_address -> district -> id"),
                    (contact_address_ward_id, AddressWard, "contact_address -> ward -> id")
                ])
                contact_address.update({
                    "address_country_id": contact_address_country_id,
                    "address_province_id": contact_address_province_id,
                    "address_district_id": contact_address_district_id,
                    "address_ward_id": contact_address_ward_id,
                    "address": contact_address_number_and_street,
                    "zip_code": None,
                    "latitude": None,
                    "longitude": None,
                    "address_primary_flag": None,
                    "address_domestic_flag": resident_address_domestic_flag,
                    "address_2": None,
                    "address_same_permanent_flag": False
                })
            ############################################################################################################

        # Nếu là địa chỉ nước ngoài
        else:
            list_require = [
                (resident_address_foreign_address_country_id, AddressCountry,
                 "resident_address -> foreign_address -> country -> id"),
                # Thành phố nước ngoài lưu vào AddressDistrict
                (resident_address_foreign_address_province_id, AddressDistrict,
                 "resident_address -> foreign_address -> province -> id"),
                # Tỉnh/Bang nước ngoài là Tỉnh/TP VN
                (resident_address_foreign_address_state_id, AddressProvince,
                 "resident_address -> foreign_address -> state -> id"),
                (contact_address_country_id, AddressCountry, "contact_address -> country -> id"),
                (contact_address_province_id, AddressProvince, "contact_address -> province -> id"),
                (contact_address_district_id, AddressDistrict, "contact_address -> district -> id"),
                (contact_address_ward_id, AddressWard, "contact_address -> ward -> id")
            ]
            list_not_null.extend(list_require)
            list_exist.extend(list_require)
            resident_address.update({
                "address_country_id": resident_address_foreign_address_country_id,
                "address_province_id": resident_address_foreign_address_state_id,
                "address_district_id": resident_address_foreign_address_province_id,
                "address_ward_id": None,
                "address": resident_address_foreign_address_address_1,
                "zip_code": resident_address_foreign_zip_code,
                "latitude": None,
                "longitude": None,
                "address_primary_flag": None,
                "address_domestic_flag": resident_address_domestic_flag,
                "address_2": resident_address_foreign_address_address_2,
                "address_same_permanent_flag": None
            })
            contact_address.update({
                "address_country_id": ADDRESS_COUNTRY_CODE_VN,
                "address_province_id": contact_address_province_id,
                "address_district_id": contact_address_district_id,
                "address_ward_id": contact_address_ward_id,
                "address": contact_address_number_and_street,
                "zip_code": None,
                "latitude": None,
                "longitude": None,
                "address_primary_flag": None,
                "address_domestic_flag": resident_address_domestic_flag,
                "address_2": None,
                "address_same_permanent_flag": None
            })
            list_not_null.extend([
                (contact_address_number_and_street, None, "contact_address -> number_and_street"),
                (resident_address_foreign_address_address_1, None, "resident_address -> foreign_address -> address_1")
            ])

        ################################################################################################################

        ################################################################################################################
        # Thông tin nghề nghiệp
        ################################################################################################################
        career_information = {
            "career_id": career_id,
            "average_income_amount_id": average_income_amount_id,
            "company_name": company_name,
            "company_phone": company_phone,
            "position_id": company_position_id,
            "company_address": company_address
        }
        list_require_career = [
            (career_id, Career, "career_information -> career -> id"),
            (average_income_amount_id, AverageIncomeAmount, "career_information -> average_income_amount -> id"),
            (company_position_id, Position, "career_information -> company_position -> id")
        ]
        list_not_null.extend(list_require_career)
        list_exist.extend(list_require_career)

        list_exist_error = check_exist_list_by_id(list_exist, session=self.oracle_session)
        list_not_null_error = check_not_null(list_not_null)

        ################################################################################################################

        # Kiểm tra những field truyền vào không được null
        if list_not_null_error:
            return self.response_exception(msg=", ".join(list_not_null_error) + " is not null")

        # Kiểm tra những field truyền vào không có trong DB
        if list_exist_error:
            return self.response_exception(msg=", ".join(list_exist_error) + " is not exist")

        contact_information_detail_data = self.call_repos(
            await repos_save_contact_information(
                cif_id=cif_id,
                created_by=self.current_user.full_name_vn,
                resident_address=resident_address,
                contact_address=contact_address,
                career_information=career_information,
                session=self.oracle_session
            )
        )
        return self.response(data=contact_information_detail_data)
