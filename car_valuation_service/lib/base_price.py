import numpy as np
import pandas as pd
from typing import List
from sklearn.base import BaseEstimator
from sklearn.linear_model import LinearRegression

import catboost as cb

from collections import defaultdict
from tqdm.notebook import tqdm


class BasePrice(BaseEstimator):

    def __init__(self, grouping_features: List[str], target_feature: str = 'actual_price') -> None:
        super().__init__()
        self.grouping_features = grouping_features
        self.target_feature = target_feature

    def fit(self, X: pd.DataFrame):
        price_grouped = X.groupby(self.grouping_features)[self.target_feature].mean().reset_index(name='base_price') # median
        self.price_grouped = price_grouped
        return self

    def predict(self, X):
        result = X.merge(self.price_grouped, how='left')
        y_pred = result['base_price'].values
        return y_pred


class DoubleRegression(BaseEstimator):

    def __init__(
            self,
            grouping_features: List[str],
            cat_features: List[str],
            num_features: List[str],
            target_feature: str = 'actual_price',
            ) -> None:
        super().__init__()
        self.grouping_features = grouping_features
        self.target_feature = target_feature
        self.cat_features = cat_features
        self.num_features = num_features
        self.features = cat_features + num_features
        self.iter = 0

    def _one_step(self, bias):
        print('--- Fitting catboost ---')
        # print(self.X[self.features].isna().sum().sum())
        # print(pd.Series(bias, name='bias').isna().sum().sum())
        self.cb_regr.fit(self.X[self.features], bias, cat_features=self.cat_features, plot=True)
        self.X[self.target_feature + '_cb'] = self.X[self.target_feature].values - self.cb_regr.predict(self.X[self.features])
        err = bias - self.X[self.target_feature + '_cb'].values
        print(f'RMSE: {np.linalg.norm(err) / np.sqrt(len(err)):.6f}, ~MedianAPE: {np.median(np.abs(np.exp(err) - 1))}')


        print('--- Fitting regressions ---')
        for name, group in tqdm(self.grouped):
            self.dict_regr[name].fit(group['age'].values.reshape(-1, 1), group[self.target_feature + '_cb'].values)
            self.X.loc[group.index, self.target_feature + '_regr'] = self.dict_regr[name].predict(group['age'].values.reshape(-1, 1))
        bias = self.X[self.target_feature].values - self.X[self.target_feature + '_regr'].values
        print(f'RMSE: {np.linalg.norm(bias) / np.sqrt(len(bias)):.6f}, ~MedianAPE: {np.median(np.abs(np.exp(bias) - 1))}')

        self.iter += 1

        return bias

    def fit(self, X: pd.DataFrame):
        X[self.target_feature + '_regr'] = X[self.target_feature].mean()
        X[self.target_feature + '_cb'] = X[self.target_feature].mean()
        self.grouped = X.groupby(self.grouping_features)[['age', self.target_feature, self.target_feature + '_cb']]
        self.X = X

        params = dict(
            learning_rate=0.5,
            iterations=500,
            reg_lambda=0.00005,
            colsample_bylevel=1.,
            max_bin=80,
            bagging_temperature=2,
            loss_function='RMSE',
            use_best_model=False,
            verbose=False,
            grow_policy='Depthwise',
            random_seed=42
        )
        self.cb_regr = cb.CatBoostRegressor(**params)

        self.dict_regr = defaultdict(LinearRegression)

        print('--- Fitting regressions ---')
        for name, group in tqdm(self.grouped):
            self.dict_regr[name].fit(group['age'].values.reshape(-1, 1), group[self.target_feature].values)
            self.X.loc[group.index, self.target_feature + '_regr'] = self.dict_regr[name].predict(group['age'].values.reshape(-1, 1))
        bias = self.X[self.target_feature].values - self.X[self.target_feature + '_regr'].values
        print(f'RMSE: {np.linalg.norm(bias) / np.sqrt(len(bias)):.6f}, ~MedianAPE: {np.median(np.abs(np.exp(bias) - 1))}')

        for _ in range(0):
            bias = self._one_step(bias)

        return self

    def predict(self, X):
        prediction = pd.Series(index=X.index, name='predict')
        grouped = X.groupby(self.grouping_features)['age']
        for name, group in grouped:
            prediction.loc[group.index] = self.dict_regr[name].predict(group.values.reshape(-1, 1))
        y_pred = prediction
        return y_pred

