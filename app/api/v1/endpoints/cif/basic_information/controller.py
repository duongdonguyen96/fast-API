from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.repository import (
    repos_get_customer_detail, repos_get_customer_personal_relationships
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.api.v1.endpoints.repository import (
    get_optional_model_object_by_code_or_name,
    repos_get_model_object_by_id_or_code
)
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.customer import CustomerGender
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.utils.constant.cif import DROPDOWN_NONE_DICT
from app.utils.error_messages import (
    ERROR_CIF_NUMBER_NOT_EXIST, ERROR_RELATION_CUSTOMER_SELF_RELATED,
    ERROR_RELATIONSHIP_EXIST, MESSAGE_STATUS
)
from app.utils.functions import dropdown


class CtrBasicInformation(BaseController):
    async def customer_detail(
            self,
            cif_id: str,
            cif_number_need_to_find: str,
            relationship_type: int
    ):
        # RULE: chỉ cif_id đang khởi tạo mới được sử dụng API này
        # check current customer is initializing
        current_customer = self.call_repos(
            await repos_get_initializing_customer(
                cif_id=cif_id,
                session=self.oracle_session
            ))

        # kiểm tra xem có đang tự quan hệ với bản thân không?
        if current_customer.cif_number == cif_number_need_to_find:
            return self.response_exception(
                msg=ERROR_RELATION_CUSTOMER_SELF_RELATED,
                loc="cif_number",
            )

        customer_detail = self.call_repos(
            await repos_get_customer_detail(
                cif_number=cif_number_need_to_find
            ))

        if not customer_detail['is_existed']:
            return self.response_exception(
                msg=ERROR_CIF_NUMBER_NOT_EXIST,
                loc="cif_number",
                detail=MESSAGE_STATUS[ERROR_CIF_NUMBER_NOT_EXIST]
            )
        else:
            customer_detail_data = customer_detail['data']

            basic_information = customer_detail_data["basic_information"]
            # map gender(str) từ Service SOA thành gender(dropdown) CRM
            basic_information_gender = basic_information["gender"]
            if basic_information_gender:
                gender = await repos_get_model_object_by_id_or_code(
                    model_id=basic_information_gender,
                    model_code=None,
                    loc="[SERVICE][SOA] gender",
                    model=CustomerGender,
                    session=self.oracle_session
                )
                basic_information["gender"] = dropdown(gender.data) if gender.data else DROPDOWN_NONE_DICT

            # map nationality(str) từ Service SOA thành nationality(dropdown) CRM
            basic_information_nationality = basic_information["nationality"]
            basic_information["nationality"] = DROPDOWN_NONE_DICT
            if basic_information_nationality:
                nationality = await repos_get_model_object_by_id_or_code(
                    model_id=basic_information_nationality,
                    model_code=None,
                    loc="[SERVICE][SOA] nationality",
                    model=AddressCountry,
                    session=self.oracle_session
                )
                if nationality.data:
                    basic_information["nationality"] = dropdown(nationality.data)

            # map place_of_issue(str) từ Service SOA thành place_of_issue(dropdown) CRM
            identity_document = customer_detail_data["identity_document"]
            basic_information_place_of_issue = identity_document["place_of_issue"]
            identity_document["place_of_issue"] = DROPDOWN_NONE_DICT
            if basic_information_place_of_issue:
                place_of_issue_model = await get_optional_model_object_by_code_or_name(
                    model=PlaceOfIssue,
                    model_code=None,
                    model_name=basic_information_place_of_issue,
                    session=self.oracle_session
                )
                if place_of_issue_model:
                    identity_document["place_of_issue"] = dropdown(place_of_issue_model)

            ############################################################################################################
            # Địa chỉ thường trú
            ############################################################################################################
            resident_address = customer_detail_data["address_information"]["resident_address"]

            # map resident_address_province(str) từ Service SOA thành resident_address_province(dropdown) CRM
            basic_information_resident_address_province = resident_address["province"]
            resident_address["province"] = DROPDOWN_NONE_DICT
            if basic_information_resident_address_province:
                resident_address_province = await repos_get_model_object_by_id_or_code(
                    model_id=None,
                    model_code=basic_information_resident_address_province,
                    loc="[SERVICE][SOA] resident_address -> province",
                    model=AddressProvince,
                    session=self.oracle_session
                )
                if resident_address_province.data:
                    resident_address["province"] = dropdown(resident_address_province.data)

            # map resident_address_district(str) từ Service SOA thành resident_address_district(dropdown) CRM
            basic_information_resident_address_district = resident_address["district"]
            resident_address["district"] = DROPDOWN_NONE_DICT
            if basic_information_resident_address_district:
                resident_address_district = await repos_get_model_object_by_id_or_code(
                    model_id=None,
                    model_code=basic_information_resident_address_district,
                    loc="[SERVICE][SOA] resident_address -> district",
                    model=AddressDistrict,
                    session=self.oracle_session
                )
                if resident_address_district.data:
                    resident_address["district"] = dropdown(resident_address_district.data)

            # map resident_address_ward(str) từ Service SOA thành resident_address_ward(dropdown) CRM
            basic_information_resident_address_ward = resident_address["ward"]
            resident_address["ward"] = DROPDOWN_NONE_DICT
            if basic_information_resident_address_ward:
                resident_address_ward = await repos_get_model_object_by_id_or_code(
                    model_id=None,
                    model_code=basic_information_resident_address_ward,
                    loc="[SERVICE][SOA] resident_address -> ward",
                    model=AddressWard,
                    session=self.oracle_session
                )
                if resident_address_ward.data:
                    resident_address["ward"] = dropdown(resident_address_ward.data)

            ############################################################################################################
            # Địa chỉ liên lạc
            ############################################################################################################
            contact_address = customer_detail_data["address_information"]["contact_address"]

            # map contact_address_province(str) từ Service SOA thành contact_address_province(dropdown) CRM
            basic_information_contact_address_province = contact_address["province"]
            contact_address["province"] = DROPDOWN_NONE_DICT
            if basic_information_contact_address_province:
                contact_address_province = await repos_get_model_object_by_id_or_code(
                    model_id=None,
                    model_code=basic_information_contact_address_province,
                    loc="[SERVICE][SOA] contact_address -> province",
                    model=AddressProvince,
                    session=self.oracle_session
                )
                if contact_address_province.data:
                    contact_address["province"] = dropdown(contact_address_province.data)

            # map contact_address_district(str) từ Service SOA thành contact_address_district(dropdown) CRM
            basic_information_contact_address_district = contact_address["district"]
            contact_address["district"] = DROPDOWN_NONE_DICT
            if basic_information_contact_address_district:
                contact_address_district = await repos_get_model_object_by_id_or_code(
                    model_id=None,
                    model_code=basic_information_contact_address_district,
                    loc="[SERVICE][SOA] contact_address -> district",
                    model=AddressDistrict,
                    session=self.oracle_session
                )
                if contact_address_district.data:
                    contact_address["district"] = dropdown(contact_address_district.data)

            # map contact_address_ward(str) từ Service SOA thành contact_address_ward(dropdown) CRM
            basic_information_contact_address_ward = contact_address["ward"]
            contact_address["ward"] = DROPDOWN_NONE_DICT
            if basic_information_contact_address_ward:
                contact_address_ward = await repos_get_model_object_by_id_or_code(
                    model_id=None,
                    model_code=basic_information_contact_address_ward,
                    loc="[SERVICE][SOA] contact_address -> ward",
                    model=AddressWard,
                    session=self.oracle_session
                )
                if contact_address_ward.data:
                    contact_address["ward"] = dropdown(contact_address_ward.data)

        relationships = await repos_get_customer_personal_relationships(
            session=self.oracle_session,
            relationship_type=relationship_type,
            cif_id=cif_id,
        )
        # kiểm tra Customer có từng quan hệ với cif_number này chưa
        if relationships:
            relationship_cif_numbers = [relationship.customer_personal_relationship_cif_number for relationship in
                                        relationships]
            if cif_number_need_to_find in relationship_cif_numbers:
                return self.response_exception(
                    msg=ERROR_RELATIONSHIP_EXIST,
                    loc="cif_number",
                )
        return self.response(data=customer_detail_data)
