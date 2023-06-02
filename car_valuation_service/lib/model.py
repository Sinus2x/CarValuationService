"""
Модуль класса Model.

Предназначен для загрузки всех необходимых
весов и классов при старте сервиса вместе с
инициализацией объекта класса и для получения
предсказаний цены авто при запросах в сервисе.
"""

from pathlib import Path
import yaml
import pandas as pd
from catboost import CatBoostRegressor
from lib.utils.load_models import load_models
from lib.utils.utils import feature_transform


CONFIG_DIR = Path(__file__).parent
CONFIG_PATH = CONFIG_DIR / "config.yaml"
with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
    CONFIG = yaml.load(config_file, Loader=yaml.FullLoader)


class Model:
    """
    Класс Model для предсказания цены автомобиля
    """
    def __init__(self):
        """
        Конструктор класса Model

        Загружает всё необходимое для обработки
        признаков и получения предсказания.
        """
        self.models_dict = load_models()
        self.model = CatBoostRegressor()
        path = Path(__file__).parent.parent / CONFIG["model_path"]
        self.model.load_model(path)

    async def predict(self, car: dict) -> int:
        """
        Метод получения предсказания цены автомобиля.

        Производит обработку признаков машины и
        получает предсказание цены
        """
        car = feature_transform(car, self.models_dict)
        col_order = self.model.feature_names_
        prediction = int(self.model.predict(car[col_order])[0])
        return prediction
