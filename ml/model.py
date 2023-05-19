from pathlib import Path
import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
from ml.utils import feature_transform
import yaml
import warnings


# load config file
config_path = Path(__file__).parent / "config.yaml"
with open(config_path, "r") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class MedianAPE:
    def __init__(self, f=lambda x: x, inv_f=lambda x: x):
        self.f = f
        self.inv_f = inv_f


    def get_final_error(self, error, weight=1.0):
        return error

    def is_max_optimal(self):
        # the lower metric value the better
        return False

    def evaluate(self, approxes, target, weight=None):
        assert len(approxes) == 1
        assert len(target) == len(approxes[0])

        approx = approxes[0]

        preds = self.inv_f(np.array(approx))
        target = self.inv_f(np.array(target))
        error = np.median((np.abs(np.subtract(target, preds) / target))) * 100
        return (error, 1.0)


class Model:
    def __init__(self):
        self.cat_features = [
        "brand", "model", "generation",
        "body_type", "drive_type", "transmission_type", "engine_type",
        "color", "pts", "owners_count", "city",
        "generation_years"
    ]

        self.num_features = [
            "doors_number",
            "year",
            "mileage",
            "horse_power",
            "month",
            "mileage_per_year",
            "base_price",
            "restyling",
            "engine_volume",
        ]

        self.emb_features = ["desc_embs", "mod_embs", "eq_embs", "tfidf_embs"]
        self.text_features = ["lemmatized_description", "brand_model_gen_res_mod", "modification", "equipment", ]
        self.params = dict(
            cat_features=self.cat_features,
            text_features=self.text_features,
            embedding_features=self.emb_features,
            learning_rate=0.05,
            iterations=5000,
            reg_lambda=0.0005,
            colsample_bylevel=1.,
            max_bin=80,
            bagging_temperature=2,
            loss_function="MAE",
            use_best_model=True,
            verbose=500,
            grow_policy="Depthwise",
            has_time=True,
            random_seed=42,
            eval_metric=MedianAPE(),
    )
        self.model = CatBoostRegressor(**self.params)
        path = Path(__file__).parent.parent / config["model_path"]
        self.model.load_model(path)

    def predict(self, x: dict) -> float:
        x = pd.Series(x).to_frame().T
        x = feature_transform(x)
        col_order = self.model.feature_names_  # catboost requires same order of cols
        preds = self.model.predict(x[col_order])
        return preds


if __name__ == "__main__":
    warnings.simplefilter("ignore")

    debug_model = Model()
    debug_car = {
        "brand": "Toyota",
        "model": "Land Cruiser Prado",
        "sale_end_date": "2023-02-10 00:00:00",
        "description": "✔ 3 ВЛАДЕЛЬЦА ПО ПТС \n✔ В РОДНОМ ОКРАСЕ\n✔ ИДЕАЛЬНОЕ ВНЕШНЕЕ СОСТОЯНИЕ\n✔ ИДЕАЛЬНОЕ ТЕХНИЧЕСКОЕ СОСТОЯНИЕ\n✔ ПОЛНОСТЬЮ ОБСЛУЖЕННЫЙ\n✔ ОБСЛУЖИВАНИЕ У ОФ. ДИЛЕРА\n✔ НЕ ТРУБУЕТ ВЛОЖЕНИЙ \n✔ KDSS ОБСЛУЖЕН\n✔ МАКСИМАЛЬНАЯ КОМПЛЕКТАЦИЯ ЛЮКС (5 МЕСТ)\n\nПродавец – крупнейший официальный дилер TOYOTA & LEXUS в Санкт-Петербурге. Более 400 а/м в наличии. 📌Кредит по двум документам 📌Одобрение кредита за 1 час и выдача автомобиля день в день 📌 Рассмотрение в 10 банках партнерах 📌 Лучшие тарифы КАСКО, ОСАГО, ГТО Все автомобили с пробегом доступны к просмотру ежедневно с 9:00, до 21:00\nОсмотреть автомобиль можно по адресу: Санкт-Петербург, Виллозское городское поселение, д. 3, строение 1\n\nМесто осмотра\n\nОсмотреть автомобиль можно по адресу: Санкт-Петербург, Виллозское городское поселение, д. 3, строение 1",
        "year": 2015,
        "generation": "150 рестайлинг (2013—2017)",
        "body_type": "Внедорожник",
        "equipment": None,
        "modification": "2.8 D AT (177 л.с.)",
        "drive_type": "Полный",
        "transmission_type": "Автомат",
        "engine_type": "Дизель",
        "doors_number": 5,
        "color": "Чёрный",
        "pts": "Дубликат",
        "owners_count": "3",
        "mileage": 260222,
        "latitude": 59.939095,
        "longitude": 30.315868,
        }

    #debug_car = pd.Series(debug_car).to_frame().T
    #debug_car = feature_transform(debug_car)
    #print(type(debug_car.desc_embs.values[0][0]))
    #print(debug_model.model.feature_names_[25])
    #print(debug_model.model.get_params())

    print(debug_model.predict(debug_car))
