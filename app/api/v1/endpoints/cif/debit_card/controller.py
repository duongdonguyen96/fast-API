from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.debit_card.repository import (
    repos_add_debit_card, repos_debit_card, repos_get_list_debit_card
)
from app.api.v1.endpoints.cif.debit_card.schema import DebitCardRequest
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.third_parties.oracle.models.master_data.address import (
    AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.card import (
    BrandOfCard, CardIssuanceFee, CardIssuanceType, CardType
)
from app.third_parties.oracle.models.master_data.customer import CustomerType
from app.utils.functions import generate_uuid, now
from app.utils.vietnamese_converter import convert_to_unsigned_vietnamese


class CtrDebitCard(BaseController):
    async def ctr_debit_card(self, cif_id: str):
        debit_card = self.call_repos(await repos_debit_card(cif_id))
        return self.response(debit_card)

    async def ctr_add_debit_card(
            self,
            cif_id: str,
            debt_card_req: DebitCardRequest
    ):
        # check, get current user
        current_user = self.call_repos(
            await repos_get_initializing_customer(
                cif_id=cif_id,
                session=self.oracle_session
            ))

        # convert last name, first name to unsigned vietnamese
        last_name = convert_to_unsigned_vietnamese(
            current_user.last_name
        )
        first_name = convert_to_unsigned_vietnamese(
            current_user.first_name
        )

        # check CardType exist
        await self.get_model_object_by_id(
            model=CardType,
            model_id=debt_card_req.issue_debit_card.physical_card_type.id,
            loc="Card Type",
        )

        # check physical_issuance_type exist
        await self.get_model_object_by_id(
            model=CardIssuanceType,
            model_id=debt_card_req.issue_debit_card.physical_issuance_type.id,
            loc="physical_issuance_type ",
        )

        # check customer_type
        await self.get_model_object_by_id(
            model=CustomerType,
            model_id=debt_card_req.issue_debit_card.customer_type.id,
            loc="customer_type",
        )

        # check branch_of_card
        await self.get_model_object_by_id(
            model=BrandOfCard,
            model_id=debt_card_req.issue_debit_card.branch_of_card.id,
            loc="branch_of_card",
        )

        # check issuance fee
        await self.get_model_object_by_id(
            model=CardIssuanceFee,
            model_id=debt_card_req.issue_debit_card.issuance_fee.id,
            loc="issuance fee",
        )

        # check province
        await self.get_model_object_by_id(
            model=AddressProvince,
            model_id=debt_card_req.card_delivery_address.delivery_address.province.id,
            loc="province",
        )

        # check district
        await self.get_model_object_by_id(
            model=AddressDistrict,
            model_id=debt_card_req.card_delivery_address.delivery_address.district.id,
            loc="district",
        )

        # check ward
        await self.get_model_object_by_id(
            model=AddressWard,
            model_id=debt_card_req.card_delivery_address.delivery_address.ward.id,
            loc="ward",
        )
        sub_card_physical_ids = []
        sub_card_issuance_ids = []
        sub_card_delivery_province_ids = []
        sub_card_delivery_district_ids = []
        sub_card_delivery_ward_ids = []
        # check information sub debit card
        for sub_card in debt_card_req.information_sub_debit_card.sub_debit_cards:
            sub_card_physical_ids.append(sub_card.physical_card_type.id)
            sub_card_issuance_ids.append(sub_card.card_issuance_type.id)
            sub_card_delivery_province_ids.append(sub_card.card_delivery_address.delivery_address.province.id)
            sub_card_delivery_district_ids.append(sub_card.card_delivery_address.delivery_address.district.id)
            sub_card_delivery_ward_ids.append(sub_card.card_delivery_address.delivery_address.ward.id)
        # check sub cardType exist
        await self.get_model_objects_by_ids(
            model_ids=sub_card_physical_ids,
            model=CardType,
            loc="sub card type",
        )
        # check physical_issuance_type exist
        await self.get_model_objects_by_ids(
            model=CardIssuanceType,
            model_ids=sub_card_issuance_ids,
            loc="sub physical_issuance_type ",
        )
        # check sub province
        await self.get_model_objects_by_ids(
            model=AddressProvince,
            model_ids=sub_card_delivery_province_ids,
            loc=" sub province",
        )

        # check sub district
        await self.get_model_objects_by_ids(
            model=AddressDistrict,
            model_ids=sub_card_delivery_district_ids,
            loc="sub district",
        )

        # check sub ward
        await self.get_model_objects_by_ids(
            model=AddressWard,
            model_ids=sub_card_delivery_ward_ids,
            loc=" sub ward",
        )

        data_card_delivery_address = {
            "id": generate_uuid(),
            "branch_id": debt_card_req.card_delivery_address.scb_branch.id,
            "province_id": debt_card_req.card_delivery_address.delivery_address.province.id,
            "district_id": debt_card_req.card_delivery_address.delivery_address.district.id,
            "ward_id": debt_card_req.card_delivery_address.delivery_address.ward.id,
            "card_delivery_address_address": debt_card_req.card_delivery_address.delivery_address.number_and_street,
            "card_delivery_address_note": debt_card_req.card_delivery_address.note,
        }

        data_debit_card = {
            "id": generate_uuid(),
            "customer_id": cif_id,
            "card_type_id": debt_card_req.issue_debit_card.physical_card_type.id,
            "card_issuance_type_id": debt_card_req.issue_debit_card.physical_issuance_type.id,
            "customer_type_id": debt_card_req.issue_debit_card.customer_type.id,
            "brand_of_card_id": debt_card_req.issue_debit_card.branch_of_card.id,
            "card_issuance_fee_id": debt_card_req.issue_debit_card.issuance_fee.id,
            "card_delivery_address_id": data_card_delivery_address['id'],
            "parent_card_id": None,
            "card_registration_flag": debt_card_req.issue_debit_card.register_flag,
            "payment_online_flag": debt_card_req.issue_debit_card.payment_online_flag,
            "first_name_on_card": first_name.upper(),  # uppercase first name
            "middle_name_on_card": debt_card_req.information_debit_card.name_on_card.middle_name_on_card.upper(),
            "last_name_on_card": last_name.upper(),  # uppercase last name
            "card_delivery_address_flag": debt_card_req.card_delivery_address.scb_delivery_address_flag,
            "created_at": now(),
            "active_flag": 1,
        }

        list_data_sub_debit_card = debt_card_req.information_sub_debit_card.sub_debit_cards
        list_sub_delivery_address = []
        list_sub_debit_card = []
        for sub_debit_card in list_data_sub_debit_card:
            list_sub_delivery_add = {
                "id": generate_uuid(),
                "branch_id": sub_debit_card.card_delivery_address.scb_branch.id,
                "province_id": sub_debit_card.card_delivery_address.delivery_address.province.id,
                "district_id": sub_debit_card.card_delivery_address.delivery_address.district.id,
                "ward_id": sub_debit_card.card_delivery_address.delivery_address.ward.id,
                "card_delivery_address_address": sub_debit_card.card_delivery_address.delivery_address.number_and_street,
                "card_delivery_address_note": sub_debit_card.card_delivery_address.note,
            }
            list_sub_delivery_address.append(list_sub_delivery_add)

            list_sub_data_debit_card = {
                "customer_id": cif_id,
                "card_type_id": sub_debit_card.physical_card_type.id,
                "card_issuance_type_id": debt_card_req.issue_debit_card.physical_issuance_type.id,
                "customer_type_id": debt_card_req.issue_debit_card.customer_type.id,
                "brand_of_card_id": debt_card_req.issue_debit_card.branch_of_card.id,
                "card_issuance_fee_id": debt_card_req.issue_debit_card.issuance_fee.id,
                "card_delivery_address_id": list_sub_delivery_add['id'],
                "parent_card_id": data_debit_card['id'],
                "card_registration_flag": debt_card_req.issue_debit_card.register_flag,
                "payment_online_flag": sub_debit_card.payment_online_flag,
                "first_name_on_card": first_name.upper(),  # uppercase first name
                "middle_name_on_card": sub_debit_card.name_on_card.middle_name_on_card.upper(),
                "last_name_on_card": last_name.upper(),  # uppercase last name
                "card_delivery_address_flag": debt_card_req.card_delivery_address.scb_delivery_address_flag,
                "created_at": now(),
                "active_flag": 1

            }
            list_sub_debit_card.append(list_sub_data_debit_card)
        add_debit_card = self.call_repos(
            await repos_add_debit_card(
                cif_id,
                data_card_delivery_address=data_card_delivery_address,
                data_debit_card=data_debit_card,
                list_sub_delivery_address=list_sub_delivery_address,
                list_sub_debit_card=list_sub_debit_card,
                session=self.oracle_session,
            )
        )
        return self.response(add_debit_card)

    async def ctr_list_debit_card_type(self, cif_id: str,
                                       branch_of_card_id: str,
                                       issuance_fee_id: str,
                                       annual_fee_id: str,
                                       ):
        info_debit_card_types = self.call_repos(
            await repos_get_list_debit_card(
                cif_id,
                branch_of_card_id,
                issuance_fee_id,
                annual_fee_id
            ))
        return self.response(info_debit_card_types)
