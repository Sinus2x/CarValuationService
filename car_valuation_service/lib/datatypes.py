"""
Модуль валидации типов в сервисе
"""

from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel


class Car(BaseModel):
    """
    Класс Car для валидации типов при подаче
    сервису входных признаков автомобиля.
    """
    brand: str
    model: str
    sale_end_date: datetime
    description: str
    year: int
    generation: str
    body_type: str
    equipment: Optional[str] = 'None'
    crashes: int = 0
    modification: str
    drive_type: str
    transmission_type: str
    engine_type: str
    doors_number: int
    color: str
    pts: Literal['Оригинал', 'Дубликат', 'Электронный'] = 'неизвестно'
    owners_count: Literal['1', '2', '3', '> 3']
    mileage: int
    latitude: float
    longitude: float


class Prediction(BaseModel):
    """
    Класс Prediction для валидации типов при
    выдаче предсказанной цены
    """
    predicted_price: int
