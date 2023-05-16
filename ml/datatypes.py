import pydantic.fields
from pydantic import BaseModel
from datetime import datetime
import typing


class Car(BaseModel):
    brand: str
    model: str
    date: datetime
    # description: str = pydantic.Field(default='', alias='text')
    year: int
    generation: str
    body_type: str
    equipment: str = ''
    modification: str
    color: str
    owners_count: typing.Literal['1', '2', '3', '> 3']
    mileage: int
    latitude: float
    longitude: float
    crashes: int
    is_taxi: typing.Literal['-1', '1', '0'] = '-1'
    is_carsharing: typing.Literal['-1', '1', '0'] = '-1'
