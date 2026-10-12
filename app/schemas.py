from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

class ShipmentCreate(BaseModel):
    reference: NonEmptyStr
    recipient: NonEmptyStr
    weight_g: int = Field(ge=1, le=20_000)

class Shipment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reference: str
    recipient: str
    weight_g: int
    status: Literal["prepared", "shipped"]
    shipping_fee: float

class Stats(BaseModel):
    prepared_count: int
    shipped_count: int
    total_shipping_fees: float