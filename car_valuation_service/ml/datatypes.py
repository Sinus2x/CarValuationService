from pydantic import BaseModel
from datetime import datetime
import typing
from typing import Optional


class Car(BaseModel):
    brand: str
    model: str
    sale_end_date: datetime
    description: str
    year: int
    generation: str
    body_type: str
    equipment: Optional[str] = 'None'
    modification: str
    drive_type: str
    transmission_type: str
    engine_type: str
    doors_number: int
    color: str
    pts: typing.Literal['Оригинал', 'Дубликат', 'Электронный'] = 'неизвестно'
    owners_count: typing.Literal['1', '2', '3', '> 3']
    mileage: int
    latitude: float
    longitude: float
