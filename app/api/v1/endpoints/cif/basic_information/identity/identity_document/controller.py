from typing import Optional, Union

from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.repository import (
    repos_get_detail_identity, repos_get_identity_information,
    repos_get_identity_log_list, repos_save_identity
)
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.schema_request import (
    CitizenCardSaveRequest, IdentityCardSaveRequest, PassportSaveRequest
)
from app.api.v1.endpoints.cif.repository import (
    repos_check_not_exist_cif_number
)
from app.third_parties.oracle.models.cif.basic_information.contact.model import (
    CustomerAddress
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.basic_information.personal.model import (
    CustomerIndividualInfo
)
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressType, AddressWard
)
from app.third_parties.oracle.models.master_data.customer import (
    CustomerClassification, CustomerEconomicProfession, CustomerGender
)
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.third_parties.oracle.models.master_data.others import Nation, Religion
from app.utils.constant.cif import (
    CONTACT_ADDRESS_CODE, CUSTOMER_UNCOMPLETED_FLAG, IDENTITY_DOCUMENT_TYPE,
    IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD, IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD,
    IDENTITY_DOCUMENT_TYPE_PASSPORT, IDENTITY_IMAGE_FLAG_BACKSIDE,
    IDENTITY_IMAGE_FLAG_FRONT_SIDE, IMAGE_TYPE_CODE_IDENTITY,
    RESIDENT_ADDRESS_CODE
)
from app.utils.error_messages import ERROR_IDENTITY_DOCUMENT_NOT_EXIST
from app.utils.functions import calculate_age, now
from app.utils.vietnamese_converter import (
    convert_to_unsigned_vietnamese, make_short_name, split_name
)


class CtrIdentityDocument(BaseController):
    async def detail_identity(self, cif_id: str):
        detail_data = self.call_repos(
            await repos_get_detail_identity(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )
        return detail_data['identity_document_type']['code'], self.response(data=detail_data)

    async def get_identity_log_list(self, cif_id: str):
        logs_data = self.call_repos(
            await repos_get_identity_log_list(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )
        return self.response(data=logs_data)

    async def save_identity(self, identity_document_request: Union[IdentityCardSaveRequest,
                                                                   CitizenCardSaveRequest,
                                                                   PassportSaveRequest]):
        if identity_document_request.identity_document_type.id not in IDENTITY_DOCUMENT_TYPE:
            return self.response_exception(msg=ERROR_IDENTITY_DOCUMENT_NOT_EXIST, loc='identity_document_type -> id')

        # trong body có truyền cif_id khác None thì lưu lại, truyền bằng None thì sẽ là tạo mới
        cif_id = identity_document_request.cif_id

        customer: Optional[Customer] = None
        customer_identity: Optional[CustomerIdentity] = None
        customer_individual_info: Optional[CustomerIndividualInfo] = None
        customer_resident_address: Optional[CustomerAddress] = None
        customer_contact_address: Optional[CustomerAddress] = None

        is_create = True
        if cif_id:
            # móc dữ liệu đã có để so sánh với identity_document_request
            customer, customer_identity, customer_individual_info, customer_resident_address, customer_contact_address \
                = self.call_repos(await repos_get_identity_information(customer_id=cif_id, session=self.oracle_session))

            is_create = False

        cif_information = identity_document_request.cif_information
        identity_document = identity_document_request.ocr_result.identity_document
        basic_information = identity_document_request.ocr_result.basic_information
        identity_document_type_id = identity_document_request.identity_document_type.id
        address_information = None
        if identity_document_type_id != IDENTITY_DOCUMENT_TYPE_PASSPORT:
            address_information = identity_document_request.ocr_result.address_information  # CMND, CCCD

        # RULE: Nếu không chọn số cif tùy chỉnh thì không được gửi cif_number lên
        if not identity_document_request.cif_information.self_selected_cif_flag \
                and identity_document_request.cif_information.cif_number:
            return self.response_exception(
                msg='',
                detail='CIF number is not allowed to be sent if self-selected CIF flag is false'
            )

        # RULE: Nếu chọn số cif tùy chỉnh thì phải gửi cif_number lên
        if identity_document_request.cif_information.self_selected_cif_flag \
                and not identity_document_request.cif_information.cif_number:
            return self.response_exception(
                msg='',
                detail='CIF number is required if self-selected CIF flag is true'
            )

        # RULE: số CIF không được khách hàng khác sử dụng
        if is_create or (customer.cif_number != cif_information.cif_number):
            self.call_repos(await repos_check_not_exist_cif_number(
                cif_number=cif_information.cif_number,
                session=self.oracle_session
            ))

        full_name_vn = identity_document_request.ocr_result.basic_information.full_name_vn
        full_name = convert_to_unsigned_vietnamese(full_name_vn)
        first_name, middle_name, last_name = split_name(full_name)
        if first_name is None and middle_name is None and last_name is None:
            return self.response_exception(msg='', detail='Can not split name to fist, middle and last name')

        customer_economic_profession_id = identity_document_request.cif_information.customer_economic_profession.id
        if is_create or (customer.customer_economic_profession_id != customer_economic_profession_id):
            await self.get_model_object_by_id(model_id=customer_economic_profession_id,
                                              model=CustomerEconomicProfession,
                                              loc='customer_economic_profession_id')

        # check customer_classification_id
        customer_classification_id = identity_document_request.cif_information.customer_classification.id
        if is_create or (customer.customer_classification_id != customer_classification_id):
            await self.get_model_object_by_id(model_id=customer_classification_id,
                                              model=CustomerClassification,
                                              loc='customer_classification_id')

        # check nationality_id
        nationality_id = basic_information.nationality.id
        if is_create or (customer_individual_info.country_of_birth_id != nationality_id):
            await self.get_model_object_by_id(model_id=nationality_id, model=AddressCountry, loc='nationality_id')

        # dict dùng để tạo mới hoặc lưu lại customer
        saving_customer = {
            "cif_number": identity_document_request.cif_information.cif_number,
            "self_selected_cif_flag": identity_document_request.cif_information.self_selected_cif_flag,
            "full_name": full_name,
            "full_name_vn": full_name_vn,
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "short_name": make_short_name(first_name, middle_name, last_name),
            "active_flag": True,
            "open_cif_at": now(),
            "open_branch_id": "000",  # TODO
            "kyc_level_id": "KYC_1",  # TODO
            "customer_category_id": "D0682B44BEB3830EE0530100007F1DDC",  # TODO
            "customer_economic_profession_id": customer_economic_profession_id,
            "nationality_id": nationality_id,
            "customer_classification_id": customer_classification_id,
            "customer_status_id": "1",  # TODO
            "channel_id": "1",  # TODO
            "avatar_url": None,
            "complete_flag": CUSTOMER_UNCOMPLETED_FLAG
        }
        ################################################################################################################

        # TODO: check identity_document bằng cách call qua eKYC

        place_of_issue_id = identity_document.place_of_issue.id
        if is_create or (customer_identity.place_of_issue_id != place_of_issue_id):
            await self.get_model_object_by_id(model_id=place_of_issue_id, model=PlaceOfIssue, loc='place_of_issue_id')

        # dict dùng để tạo mới hoặc lưu lại customer_identity
        saving_customer_identity = {
            "identity_type_id": identity_document_request.identity_document_type.id,
            "identity_num": identity_document.identity_number,
            "issued_date": identity_document.issued_date,
            "expired_date": identity_document.expired_date,
            "place_of_issue_id": place_of_issue_id,
            "maker_at": now(),
            "maker_id": self.current_user.user_id,
            "updater_at": now(),
            "updater_id": self.current_user.user_id
        }

        gender_id = basic_information.gender.id
        if is_create or (customer_individual_info.gender_id != gender_id):
            await self.get_model_object_by_id(model_id=gender_id, model=CustomerGender, loc='gender_id')

        religion_id = None
        ethnic_id = None
        identity_characteristic = None
        father_full_name_vn = None
        mother_full_name_vn = None
        if identity_document_type_id == IDENTITY_DOCUMENT_TYPE_PASSPORT:
            province_id = basic_information.place_of_birth.id
        else:
            province_id = basic_information.province.id
            identity_characteristic = basic_information.identity_characteristic
            if identity_document_type_id == IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD:
                # check ethnic_id
                ethnic_id = basic_information.ethnic.id
                if is_create or (customer_individual_info.nation_id != ethnic_id):
                    await self.get_model_object_by_id(model_id=ethnic_id, model=Nation, loc='ethnic_id')

                # check religion_id
                religion_id = basic_information.religion.id
                if is_create or (customer_individual_info.religion_id != religion_id):
                    await self.get_model_object_by_id(model_id=religion_id, model=Religion, loc='religion_id')

                father_full_name_vn = basic_information.father_full_name_vn
                mother_full_name_vn = basic_information.mother_full_name_vn

        # check place_of_birth or province.id        # check place_of_birth or province.id
        if is_create or (customer_individual_info.place_of_birth_id != province_id):
            await self.get_model_object_by_id(model_id=province_id, model=AddressProvince, loc='province_id')

        # dict dùng để tạo mới hoặc lưu lại customer_individual_info
        saving_customer_individual_info = {
            "gender_id": gender_id,
            "place_of_birth_id": province_id,
            "country_of_birth_id": nationality_id,
            "religion_id": religion_id,
            "nation_id": ethnic_id,
            "date_of_birth": basic_information.date_of_birth,
            "under_15_year_old_flag": True if calculate_age(basic_information.date_of_birth) < 15 else False,
            "identifying_characteristics": identity_characteristic,
            "father_full_name": father_full_name_vn,
            "mother_full_name": mother_full_name_vn
        }

        ################################################################################################################

        if identity_document_type_id != IDENTITY_DOCUMENT_TYPE_PASSPORT:
            resident_address = await self.get_model_object_by_code(
                model_code=RESIDENT_ADDRESS_CODE, model=AddressType, loc='resident_address'
            )
            # check resident_address_province_id
            resident_address_province_id = address_information.resident_address.province.id
            if is_create or (customer_resident_address.address_province_id != resident_address_province_id):
                await self.get_model_object_by_id(model_id=resident_address_province_id, model=AddressProvince,
                                                  loc='resident_address -> province -> id')

            # check resident_address_district_id
            resident_address_district_id = address_information.resident_address.district.id
            if is_create or (customer_resident_address.address_district_id != resident_address_district_id):
                await self.get_model_object_by_id(model_id=resident_address_district_id, model=AddressDistrict,
                                                  loc='resident_address -> district -> id')

            # check resident_address_ward_id
            resident_address_ward_id = address_information.resident_address.ward.id
            if is_create or (customer_resident_address.address_ward_id != resident_address_ward_id):
                await self.get_model_object_by_id(model_id=resident_address_ward_id, model=AddressWard,
                                                  loc='resident_address -> ward -> id')

            # dict dùng để tạo mới hoặc lưu lại customer_resident_address
            saving_customer_resident_address = {
                "address_type_id": resident_address.id,
                "address_country_id": nationality_id,
                "address_province_id": resident_address_province_id,
                "address_district_id": resident_address_district_id,
                "address_ward_id": resident_address_ward_id,
                "address": address_information.resident_address.number_and_street
            }
            ###########################################################################################################

            contact_address = await self.get_model_object_by_code(
                model_code=CONTACT_ADDRESS_CODE, model=AddressType, loc='resident_address'
            )

            # check contact_address_province_id
            contact_address_province_id = address_information.contact_address.province.id
            if is_create or (customer_contact_address.address_province_id != contact_address_province_id):
                await self.get_model_object_by_id(model_id=contact_address_province_id, model=AddressProvince,
                                                  loc='contact_address -> province -> id')

            # check contact_address_district_id
            contact_address_district_id = address_information.contact_address.district.id
            if is_create or (customer_contact_address.address_district_id != contact_address_district_id):
                await self.get_model_object_by_id(model_id=contact_address_district_id, model=AddressDistrict,
                                                  loc='contact_address -> district -> id')

            # check contact_address_ward_id
            contact_address_ward_id = address_information.contact_address.ward.id
            if is_create or (customer_contact_address.address_ward_id != contact_address_ward_id):
                await self.get_model_object_by_id(model_id=contact_address_ward_id, model=AddressWard,
                                                  loc='contact_address -> ward -> id')

            # dict dùng để tạo mới hoặc lưu lại customer_contact_address
            saving_customer_contact_address = {
                "address_type_id": contact_address.id,
                "address_country_id": nationality_id,
                "address_province_id": contact_address_province_id,
                "address_district_id": contact_address_district_id,
                "address_ward_id": contact_address_ward_id,
                "address": address_information.contact_address.number_and_street
            }
            ############################################################################################################

            if identity_document_type_id == IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD:
                saving_customer_identity.update({
                    "qrcode_content": identity_document_request.ocr_result.identity_document.qr_code_content,
                    "mrz_content": identity_document_request.ocr_result.identity_document.mrz_content
                })
            ############################################################################################################

            front_side_information_identity_image_url = identity_document_request.front_side_information.identity_image_url
            back_side_information_identity_image_url = identity_document_request.back_side_information.identity_image_url
            compare_image_url = identity_document_request.front_side_information.face_compare_image_url

            saving_customer_identity_images = [
                {
                    "image_type_id": IMAGE_TYPE_CODE_IDENTITY,
                    "image_url": front_side_information_identity_image_url,
                    "hand_side_id": None,
                    "finger_type_id": None,
                    "vector_data": None,
                    "active_flag": True,
                    "maker_id": self.current_user.user_id,
                    "maker_at": now(),
                    "updater_id": self.current_user.user_id,
                    "updater_at": now(),
                    "identity_image_front_flag": IDENTITY_IMAGE_FLAG_FRONT_SIDE
                },
                {
                    "image_type_id": IMAGE_TYPE_CODE_IDENTITY,
                    "image_url": back_side_information_identity_image_url,
                    "hand_side_id": None,
                    "finger_type_id": None,
                    "vector_data": None,
                    "active_flag": True,
                    "maker_id": self.current_user.user_id,
                    "updater_at": now(),
                    "identity_image_front_flag": IDENTITY_IMAGE_FLAG_BACKSIDE
                }
            ]

        # HO_CHIEU
        else:
            saving_customer_resident_address = None
            saving_customer_contact_address = None
            saving_customer_identity.update({
                "passport_type_id": identity_document_request.ocr_result.identity_document.passport_type.id,
                "passport_code_id": identity_document_request.ocr_result.identity_document.passport_code.id,
                "identity_number_in_passport": identity_document_request.ocr_result.basic_information.identity_card_number,
                "mrz_content": identity_document_request.ocr_result.basic_information.mrz_content
            })
            ############################################################################################################

            compare_image_url = identity_document_request.passport_information.face_compare_image_url
            saving_customer_identity_images = [{
                "image_type_id": IMAGE_TYPE_CODE_IDENTITY,
                "image_url": identity_document_request.passport_information.identity_image_url,
                "hand_side_id": None,
                "finger_type_id": None,
                "vector_data": None,
                "active_flag": True,
                "maker_id": self.current_user.user_id,
                "maker_at": now(),
                "updater_id": self.current_user.user_id,
                "updater_at": now(),
                "identity_image_front_flag": None
            }]

        # dict dùng để tạo mới hoặc lưu lại CustomerCompareImage
        saving_customer_compare_image = {
            "compare_image_url": compare_image_url,
            "similar_percent": 00,  # TODO: gọi qua eKYC để check
            "maker_id": self.current_user.user_id,
            "maker_at": now()
        }
        ############################################################################################################

        info_save_document = self.call_repos(
            await repos_save_identity(
                identity_document_type_id=identity_document_type_id,
                customer_id=None if is_create else customer.id,
                identity_id=None if is_create else customer_identity.id,
                saving_customer=saving_customer,
                saving_customer_identity=saving_customer_identity,
                saving_customer_individual_info=saving_customer_individual_info,
                saving_customer_resident_address=saving_customer_resident_address,
                saving_customer_contact_address=saving_customer_contact_address,
                saving_customer_compare_image=saving_customer_compare_image,
                saving_customer_identity_images=saving_customer_identity_images,
                log_data=identity_document_request.json(),
                session=self.oracle_session
            )
        )
        return self.response(data=info_save_document)
