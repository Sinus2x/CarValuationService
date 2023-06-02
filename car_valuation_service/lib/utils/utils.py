"""
Модуль для преобразования переданных в сервис
признаков автомобиля для последующей передачи
и получения предсказания цены.
"""

import pandas as pd
from lib.utils.nan_fill import fill_na_transform
from lib.utils.add_features import features_extract
from lib.utils.add_text_features import text_features_extract


def feature_transform(car: dict, models_dict: dict) -> pd.DataFrame:
    """
    Функция преобразования признаков автомобиля
    """
    car['sale_end_date'] = pd.to_datetime(car['sale_end_date'])
    transformations = [
        fill_na_transform,
        features_extract,
        text_features_extract
    ]
    for transform in transformations:
        car = transform(car, models_dict)
    car = pd.Series(car).to_frame().T
    return car
