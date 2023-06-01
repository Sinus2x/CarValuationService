import numpy as np
import pandas as pd
from typing import List
from enum import Enum
from sklearn.base import BaseEstimator
from sklearn.linear_model import LinearRegression, QuantileRegressor
from sklearn.isotonic import IsotonicRegression

from scipy.stats import gmean, hmean, trim_mean, boxcox
from scipy.special import inv_boxcox
from scipy.stats.mstats import trimmed_mean

import catboost as cb

from collections import defaultdict
from collections import namedtuple
from tqdm.notebook import trange, tqdm


def find_optimal(x):
        sorted_x = np.sort(x)
        n = (len(x) - 1) // 2
        optimal_k = n
        if n != 0:
            optimal_k = np.array([sorted_x[idx + n] / sorted_x[idx] for idx in range(n)]).argmin()
        res = hmean([sorted_x[optimal_k], sorted_x[optimal_k + n]])
        return res


def identity(x):
    return x


class BasePrice(BaseEstimator):
    '''
    Класс для получения базовых цен каждой группы машин.

    `BasePrice` поддерживает разные способы получения "средней"
    цены внутри группы машин (mean, median, harmonic mean и т.д.).
    "Усреднение" проводится с учетом иерархии признаков,
    чтобы не было NaN.

    Есть дополнительный параметр отвечающий за "усечение" данных
    (trimming или outlier detector) перед получением "средней" цены.

    Parameters
    ----------
    grouping_features : List[str]
        Список признаков для группировки.
    target_feature : str
        Название целевого признака.
    target_mode : str
        Вид трансформации целевого признака.
    avg_mode : str
        Способ получения "средней" цены внутри группы.
    trim_mode : str
        Способ "усечения" данных.

    Attributes
    ----------
    target_modes : dict
        Словарь, содержащий все способы трансформации целевого признака.
    avg_modes : dict
        Словарь, содержащий все способы получения "средней" цены.
    trim_modes : dict
        Словарь, содержащий все способы "усечения" данных.

    Notes
    -----

    Examples
    -----

    '''

    target_modes = {
        'identity': (identity, identity),
        'log': (np.log, np.exp),
        'boxcox': (boxcox, inv_boxcox)
    }

    avg_modes = {
        'mean': np.mean,
        'median': np.median,
        'geometric': gmean,
        'harmonic': hmean,
        'group_optimal': find_optimal,
    }

    trim_modes = {
        'empty': identity,
    }

    def __init__(
            self,
            grouping_features: List[str],
            target_feature: str = 'actual_price',
            target_mode: str = 'identity',
            avg_mode: str = 'mean',
            trim_mode: str = 'empty',
            min_count = 3
            ) -> None:
        super().__init__()
        self.grouping_features = grouping_features
        self.target_feature = target_feature

        self.target_mode = target_mode
        self.target_method = self.target_modes[target_mode]

        self.avg_mode = avg_mode
        self.avg_method = self.avg_modes[avg_mode]

        self.trim_mode = trim_mode
        self.trim_method = self.trim_modes[trim_mode]

        self.min_count = min_count

    def fit(self, X: pd.DataFrame):
        self.dict_price_grouped = dict()
        grouped = X.groupby(self.grouping_features)[self.target_feature]
        for idx in range(len(self.grouping_features), 0, -1):
            grouped = X.groupby(self.grouping_features[:idx])[self.target_feature]
            price_grouped = grouped.agg([('base_price', lambda x: np.nan)])
            for name, group in grouped:
                temp = self.trim_method(group.values)
                if len(temp) < self.min_count:
                    continue
                if self.target_mode == 'boxcox':
                    temp, fitted_lmbda = self.target_method[0](temp)
                else:
                    temp = self.target_method[0](temp)
                temp = self.avg_method(temp)
                if self.target_mode == 'boxcox':
                    temp = self.target_method[1](temp, fitted_lmbda)
                price_grouped.loc[name] = temp

            self.dict_price_grouped[tuple(self.grouping_features[:idx])] = price_grouped.reset_index()

        return self

    def predict(self, X):
        mask = np.full(X.shape[0], True)
        result = np.full(X.shape[0], np.nan)
        for idx in range(len(self.grouping_features), 0, -1):
            masked_X = X[mask]
            price_grouped = self.dict_price_grouped[tuple(self.grouping_features[:idx])]
            result[mask] = masked_X.merge(price_grouped, how='left')['base_price'].values
            mask = np.isnan(result)
            if not mask.any():
                break

        return result

    # нужно хранить в другом виде price_grouped
    # чтобы сразу были нужные поля в виде индексов
    # def predict_obj(self, obj):
    #     result = np.nan
    #     for idx in range(len(self.grouping_features), 0, -1):
    #         x = tuple(obj[key] for key in self.grouping_features[:idx])
    #         price_grouped = self.dict_price_grouped[tuple(self.grouping_features[:idx])]
    #         mask = price_grouped[]
    #         result = masked_X.merge(price_grouped, how='left')['base_price'].values
    #         if not np.isnan(result):
    #             break

    #     return result


def test_get_base_price(df: pd.DataFrame) -> pd.DataFrame:
    def predict(X, price_grouped, grouping_features):
        ###
        # load part
        ###
        dict_price_grouped = dict()
        for idx in range(len(grouping_features), 0, -1):
            grouped = price_grouped.groupby(grouping_features[:idx])['base_price']
            new_price_grouped = grouped.agg([('new_base_price', lambda x: np.nan)])
            for name, group in grouped:
                new_price_grouped.loc[name] = np.mean(group.values)

            dict_price_grouped[tuple(grouping_features[:idx])] = new_price_grouped.reset_index()

        ###
        # predict part
        ###
        mask = np.full(X.shape[0], True)
        result = np.full(X.shape[0], np.nan)
        for idx in range(len(grouping_features), 0, -1):
            masked_X = X[mask]
            new_price_grouped = dict_price_grouped[tuple(grouping_features[:idx])]
            result[mask] = masked_X.merge(new_price_grouped, how='left')['new_base_price'].values
            mask = np.isnan(result)
            if not mask.any():
                break
        return result

    base_price_grouper_cols = ['brand', 'model', 'generation', 'modification']
    base_price_grouper = pd.read_csv("base_price_grouper.csv")
    df['base_price'] = predict(df, base_price_grouper, base_price_grouper_cols)
    return df
