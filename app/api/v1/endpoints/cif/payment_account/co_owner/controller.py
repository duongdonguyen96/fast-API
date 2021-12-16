from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.payment_account.co_owner.repository import (
    repos_detail_co_owner, repos_get_co_owner_data, repos_save_co_owner
)
from app.api.v1.endpoints.cif.payment_account.co_owner.schema import (
    AccountHolderRequest
)
from app.utils.constant.cif import CONTACT_ADDRESS_CODE, RESIDENT_ADDRESS_CODE
from app.utils.functions import dropdown


class CtrCoOwner(BaseController):
    async def ctr_save_co_owner(self, cif_id: str, co_owner: AccountHolderRequest):
        co_owner_data = self.call_repos(
            await repos_save_co_owner(
                cif_id,
                co_owner,
                created_by=self.current_user.full_name_vn
            )
        )

        return self.response(data=co_owner_data)

    async def ctr_co_owner(self, cif_id: str):
        co_owner_data = self.call_repos(await repos_get_co_owner_data(cif_id))

        return self.response(data=co_owner_data)

    async def detail_co_owner(self, cif_id: str, cif_number_need_to_find: str):

        detail_co_owner = self.call_repos(await repos_detail_co_owner(
            cif_id=cif_id,
            cif_number_need_to_find=cif_number_need_to_find,
            session=self.oracle_session
        ))

        resident_address = None
        contact_address = None

        for row in detail_co_owner:
            if row.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
                resident_address = row.CustomerAddress.address
            if row.CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE:
                contact_address = row.CustomerAddress.address

        first_row = detail_co_owner[0]

        # lọc giá trị trùng chữ ký khi query
        customer__signature = {}
        for signature in detail_co_owner:
            if signature.CustomerIdentityImage.id not in customer__signature:
                customer__signature[signature.CustomerIdentityImage.id] = []
                customer__signature[signature.CustomerIdentityImage.id].append({
                    'id': signature.CustomerIdentityImage.id,
                    'image_url': signature.CustomerIdentityImage.image_url
                })

        signature = []
        for customer_signature in customer__signature.values():
            signature.extend(customer_signature)

        response_data = {
            "id": first_row.Customer.id,
            "basic_information": {
                "full_name_vn": first_row.Customer.full_name_vn,
                "cif_number": first_row.Customer.cif_number,
                "date_of_birth": first_row.CustomerIndividualInfo.date_of_birth,
                "customer_relationship": dropdown(first_row.CustomerRelationshipType),
                "nationality": dropdown(first_row.AddressCountry),
                "gender": dropdown(first_row.CustomerGender),
                "mobile_number": first_row.Customer.mobile_number,
                "signature": signature
            },
            "identity_document": {
                "identity_number": first_row.CustomerIdentity.identity_num,
                "identity_type": dropdown(first_row.CustomerIdentityType),
                "issued_date": first_row.CustomerIdentity.issued_date,
                "expired_date": first_row.CustomerIdentity.expired_date,
                "place_of_issue": dropdown(first_row.PlaceOfIssue)
            },
            "address_information": {
                'contact_address': contact_address,
                'resident_address': resident_address
            }
        }
        return self.response(data=response_data)
