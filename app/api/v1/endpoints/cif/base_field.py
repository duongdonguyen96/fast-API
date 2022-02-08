from typing import Optional

from pydantic import Field

CIF_NUMBER_MIN_LENGTH = 7
CIF_NUMBER_MAX_LENGTH = 7

STR_MIN_LENGTH = 1


class CustomField:
    def __init__(self, description: str = "Số CIF", min_length: Optional[int] = None, max_length: Optional[int] = None):
        """
        CIFNumberField: Field CIF Number với giá trị là bắt buộc nhập
        OptionalCIFNumberField: Field CIF Number với giá trị là không bắt buộc nhập
        """
        self.description = description
        self.min_length = min_length
        self.max_length = max_length

        self.CIFNumberField = Field(..., description=self.description, min_length=CIF_NUMBER_MIN_LENGTH,
                                    max_length=CIF_NUMBER_MAX_LENGTH)
        self.OptionalCIFNumberField = Field(None, description=self.description, min_length=CIF_NUMBER_MIN_LENGTH,
                                            max_length=CIF_NUMBER_MAX_LENGTH)
