from typing import List

import pandas as pd
from sklearn.base import BaseEstimator


class BasePrice(BaseEstimator):

    def __init__(self, grouping_features: List[str], target_feature: str = 'actual_price') -> None:
        super().__init__()
        self.grouping_features = grouping_features
        self.target_feature = target_feature
        self.price_grouped = None

    def fit(self, X: pd.DataFrame):
        grouped = X.groupby(self.grouping_features)[self.target_feature]
        self.price_grouped = grouped.mean().reset_index(name='base_price')
        return self

    def predict(self, X: pd.DataFrame):
        result = X.merge(self.price_grouped, how='left')
        y_pred = result['base_price'].values
        return y_pred
