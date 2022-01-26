from pydantic import Field


def CIFNumberField(description: str):
    return Field(..., description=description, min_length=7, max_length=7)
