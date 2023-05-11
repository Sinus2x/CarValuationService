from pathlib import Path
import pandas as pd
from catboost import CatBoostRegressor
from ml.utils import get_city
import yaml


# load config file
config_path = Path(__file__).parent / "config.yaml"
with open(config_path, "r") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Model:
    def __init__(self):
        self.model = CatBoostRegressor()
        path = Path(__file__).parent.parent / config['model_path']
        self.model.load_model(path)

    @staticmethod
    def get_horsepower(mod: str):
        bracket = mod.find('(')
        last = mod.find(')')
        return int(mod[bracket + 1:last].split()[0])

    def predict(self, x: dict) -> float:
        x = pd.Series(x)
        x['horsepower'] = self.get_horsepower(x['modification'])
        x['month'] = int(x['date'].month)
        x['city'] = get_city(x['latitude'], x['longitude'])
        x['sale_year'] = int(x['date'].year)
        col_order = self.model.feature_names_  # catboost requires same order of cols
        pred = self.model.predict(x[col_order])
        return pred