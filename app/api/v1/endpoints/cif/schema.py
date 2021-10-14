from app.api.base.base_schema import CustomBaseModel


class CustomerClassification(CustomBaseModel):
    id: str
    code: str
    name: str


class CustomerEconomicProfession(CustomBaseModel):
    id: str
    code: str
    name: str


class KYCLevel(CustomBaseModel):
    id: str
    code: str
    name: str


class CifInformationRes(CustomBaseModel):
    self_selected_cif_flag: bool
    cif_number: str
    customer_classification: CustomerClassification
    customer_economic_profession: CustomerEconomicProfession
    kyc_level: KYCLevel
