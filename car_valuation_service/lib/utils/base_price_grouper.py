"""
    Модуль, в котором содержится класс `BasePriceGrouper`.
    Этот класс нужен для получения базовой цены машины.
"""

from operator import itemgetter
import pandas as pd


class BasePriceGrouper:
    """
    Класс `BasePriceGrouper` для получения базовой цены машины
    с учётом последовательности признаков при группировки.
    """

    def __init__(self, df_groups: pd.DataFrame) -> None:
        self.grouping_features = df_groups.columns[:-1].to_list()
        self.target_feature = df_groups.columns[-1]
        self.dict_price_grouped = {}
        self.get_car_features = itemgetter(*self.grouping_features)

        self._build(df_groups)

    def _build(self, df_groups: pd.DataFrame) -> None:
        """
        Приватный метод для построения объекта класса.
        Последовательно усредняет группировки по последовательности признаков.
        """
        for idx in range(len(self.grouping_features), 0, -1):
            current_features = self.grouping_features[:idx]
            grouped = df_groups.groupby(current_features)[self.target_feature]
            self.dict_price_grouped[tuple(current_features)] = grouped.agg('mean')

    def predict(self, car: dict) -> float:
        """
        Определяет базовую цены для машины,
        используя последовательные группировки.
        """
        car_features = self.get_car_features(car)
        for idx in range(len(self.grouping_features), 0, -1):
            current_features = tuple(self.grouping_features[:idx])
            base_price = self.dict_price_grouped[current_features].get(car_features[:idx], 0.0)
            if base_price > 0:
                break
        return base_price
