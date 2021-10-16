from app.api.base.schema import BaseSchema


class CustomerClassification(BaseSchema):
    id: str
    code: str
    name: str


class CustomerEconomicProfession(BaseSchema):
    id: str
    code: str
    name: str


class KYCLevel(BaseSchema):
    id: str
    code: str
    name: str


class CifInformationRes(BaseSchema):
    self_selected_cif_flag: bool
    cif_number: str
    customer_classification: CustomerClassification
    customer_economic_profession: CustomerEconomicProfession
    kyc_level: KYCLevel
