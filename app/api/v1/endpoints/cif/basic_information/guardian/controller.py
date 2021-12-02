from typing import List

from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.guardian.repository import (
    repos_get_guardians, repos_save_guardians
)
from app.api.v1.endpoints.cif.basic_information.guardian.schema import (
    SaveGuardianRequest
)
from app.api.v1.endpoints.cif.repository import (
    repos_get_customers_by_cif_numbers, repos_get_initializing_customer
)
from app.api.v1.endpoints.repository import repos_get_model_objects_by_ids
from app.third_parties.oracle.models.master_data.customer import (
    CustomerRelationshipType
)
from app.utils.constant.cif import CUSTOMER_RELATIONSHIP_TYPE_GUARDIAN
from app.utils.error_messages import (
    ERROR_CIF_NUMBER_DUPLICATED, ERROR_RELATION_CUSTOMER_SELF_RELATED
)


class CtrGuardian(BaseController):
    async def detail(self, cif_id: str):
        detail_guardian_info = self.call_repos(
            await repos_get_guardians(
                session=self.oracle_session,
                cif_id=cif_id
            ))

        return self.response(data=detail_guardian_info)

    async def save(self,
                   cif_id: str,
                   guardian_save_request: List[SaveGuardianRequest]):
        # check and get current customer
        current_customer = self.call_repos(
            await repos_get_initializing_customer(
                cif_id=cif_id,
                session=self.oracle_session
            ))

        guardian_cif_numbers, relationship_types = [], set()
        for guardian in guardian_save_request:
            guardian_cif_numbers.append(guardian.cif_number),
            relationship_types.add(guardian.customer_relationship.id)

        # check duplicate cif_number in request body
        if len(guardian_cif_numbers) != len(set(guardian_cif_numbers)):
            return self.response_exception(
                msg=ERROR_CIF_NUMBER_DUPLICATED,
                loc="cif_number",
            )

        # check if it relates to itself
        if current_customer.cif_number in guardian_cif_numbers:
            return self.response_exception(
                msg=ERROR_RELATION_CUSTOMER_SELF_RELATED,
                loc="cif_number",
            )

        # check cif_number exist and get guardian's
        guardians = self.call_repos(
            await repos_get_customers_by_cif_numbers(
                cif_numbers=guardian_cif_numbers,
                session=self.oracle_session
            )
        )

        # check relationship types exist
        await repos_get_model_objects_by_ids(
            model=CustomerRelationshipType,
            model_ids=list(relationship_types),
            session=self.oracle_session,
            loc="customer_relationship"
        )

        guardians_cif_number__id = {}
        for guardian in guardians:
            guardians_cif_number__id[guardian.cif_number] = guardian.id
        list_data_insert = [{
            "customer_id": cif_id,
            "customer_relationship_type_id": guardian.customer_relationship.id,
            "type": CUSTOMER_RELATIONSHIP_TYPE_GUARDIAN,
            "customer_personal_relationship_cif_number": guardian.cif_number,
            "customer_relationship_id": guardians_cif_number__id[guardian.cif_number]
        } for guardian in guardian_save_request]

        save_guardian_info = self.call_repos(
            await repos_save_guardians(
                cif_id=cif_id,
                list_data_insert=list_data_insert,
                created_by=self.current_user.full_name_vn,
                session=self.oracle_session
            ))

        return self.response(data=save_guardian_info)
