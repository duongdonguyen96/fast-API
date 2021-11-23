from typing import Union

from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.repository import (
    repos_get_detail, repos_get_list_log, repos_save_identity
)
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.schema_request import (
    CitizenCardSaveRequest, IdentityCardSaveRequest, PassportSaveRequest
)
from app.third_parties.oracle.models.master_data.address import AddressCountry, AddressProvince, AddressDistrict, \
    AddressWard
from app.third_parties.oracle.models.master_data.customer import CustomerGender
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.third_parties.oracle.models.master_data.others import Nation, Religion
from app.utils.constant.cif import IDENTITY_DOCUMENT_TYPE
from app.utils.error_messages import ERROR_IDENTITY_DOCUMENT_NOT_EXIST
from app.utils.functions import check_exist_list_by_id, raise_does_not_exist_string
from app.utils.vietnamese_converted import split_name


class CtrIdentityDocument(BaseController):
    async def detail(self, cif_id: str, identity_document_type_id: str):
        detail_data = self.call_repos(
            await repos_get_detail(
                cif_id=cif_id,
                identity_document_type_id=identity_document_type_id
            )
        )
        return self.response(data=detail_data)

    async def get_list_log(self, cif_id: str):
        logs_data = self.call_repos(
            await repos_get_list_log(cif_id=cif_id)
        )
        return self.response(data=logs_data)

    async def save_identity(
            self,
            identity_document_req: Union[IdentityCardSaveRequest, CitizenCardSaveRequest, PassportSaveRequest]
    ):
        # trong body có truyền cif_id khác None thì lưu lại, truyền bằng None thì sẽ là tạo mới
        if identity_document_req.identity_document_type.id not in IDENTITY_DOCUMENT_TYPE:
            return self.response_exception(msg=ERROR_IDENTITY_DOCUMENT_NOT_EXIST, loc='identity_document_type -> id')

        place_of_issue_id = identity_document_req.ocr_result.identity_document.place_of_issue.id
        gender_id = identity_document_req.ocr_result.basic_information.gender.id
        nationality_id = identity_document_req.ocr_result.basic_information.nationality.id
        province_id = identity_document_req.ocr_result.basic_information.province.id
        ethnic_id = identity_document_req.ocr_result.basic_information.ethnic.id
        religion_id = identity_document_req.ocr_result.basic_information.religion.id
        resident_address_province_id = identity_document_req.ocr_result.address_information.resident_address.province.id
        resident_address_district_id = identity_document_req.ocr_result.address_information.resident_address.district.id
        resident_address_ward_id = identity_document_req.ocr_result.address_information.resident_address.ward.id
        contact_address_province_id = identity_document_req.ocr_result.address_information.contact_address.province.id
        contact_address_district_id = identity_document_req.ocr_result.address_information.contact_address.district.id
        contact_address_ward_id = identity_document_req.ocr_result.address_information.contact_address.ward.id

        list_exist = [
            (place_of_issue_id, PlaceOfIssue, "place_of_issue_id"),
            (gender_id, CustomerGender, "gender_id"),
            (nationality_id, AddressCountry, "nationality_id"),
            (province_id, AddressProvince, "province_id"),
            (ethnic_id, Nation, "ethnic_id"),
            (religion_id, Religion, "religion_id"),
            (resident_address_province_id, AddressProvince, "resident_address_province_id"),
            (resident_address_district_id, AddressDistrict, "resident_address_district_id"),
            (resident_address_ward_id, AddressWard, "resident_address_ward_id"),
            (contact_address_province_id, AddressProvince, "contact_address_province_id"),
            (contact_address_district_id, AddressDistrict, "contact_address_district_id"),
            (contact_address_ward_id, AddressWard, "contact_address_ward_id"),
        ]
        list_error = check_exist_list_by_id(list_exist, session=self.oracle_session)
        if list_error:
            return self.response_exception(msg=raise_does_not_exist_string(", ".join(list_error)),
                                           loc=", ".join(list_error))

        full_name_vn = identity_document_req.ocr_result.basic_information.full_name_vn
        if not split_name(full_name_vn):
            return self.response_exception(msg="Invalid name length (length <= 1)", loc="full_name_vn")


        info_save_document = self.call_repos(
            await repos_save_identity(
                identity_document_req=identity_document_req,
                save_by=self.current_user.user_id,
                session=self.oracle_session
            )
        )
        return self.response(data=info_save_document)
