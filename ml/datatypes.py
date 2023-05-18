import pandas as pd
import pydantic.fields
from pydantic import BaseModel
from datetime import datetime
import typing


class Car(BaseModel):
    brand: str
    model: str
    sale_end_date: datetime
    description: str  # = pydantic.Field(default='', alias='text')
    year: int
    generation: str
    body_type: str
    equipment: str
    modification: str
    drive_type: str
    transmission_type: str
    engine_type: str
    doors_number: int
    color: str
    pts: str
    owners_count: typing.Literal['1', '2', '3', '> 3']
    mileage: int
    latitude: float
    longitude: float
