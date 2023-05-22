from pathlib import Path
import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
from ml.utils import feature_transform
from ml.load_models import load_models
import yaml
import time


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
        self.models_dict = load_models()
        self.model = CatBoostRegressor(**self.params)
        path = Path(__file__).parent.parent / config["model_path"]
        self.model.load_model(path)

    async def predict(self, x: dict) -> float:
        x = pd.Series(x).to_frame().T
        time_start = time.time()
        x = feature_transform(x, self.models_dict)
        time_end_transform = time.time()
        col_order = self.model.feature_names_
        preds = self.model.predict(x[col_order])
        time_end_predict = time.time()
        print(f"Sum time for features transform - {time_end_transform - time_start} seconds")
        print(f"Predict - {time_end_predict - time_end_transform} seconds")
        print(f"Sum time for predict and transform - {time_end_predict - time_start} seconds")
        return preds


if __name__ == "__main__":
    import asyncio
    import warnings

    warnings.simplefilter("ignore")

    car = {
        "actual_price": 5200000.0,
        "brand": "Porsche",
        "model": "Cayenne",
        "sale_end_date": "2022-11-26 00:00:00",
        "description": "🔥🔥🔥СПЕЦПРЕДЛОЖЕНИЕ!!!🔥🔥🔥 \n\n🚙 Porsche Cayenne III\n\n    ✅ WP1ZZZ9YZKDA05407\n\n⚡ Автомобиль из Европы!!! Идеальное состояние!!!\n\n   ✅1 Владелец. ЭПТС\n   ✅Полностью в родном окрасе.\n   ✅ОТЛИЧНЫЙ ВНЕШНИЙ ВИД\n   ✅ЧИСТЫЙ УХОЖЕННЫЙ САЛОН\n   ✅АВТОМОБИЛЬ ПРОШЕЛ КОМПЛЕКСНУЮ И КРИМИНАЛИСТИЧЕСКУЮ ДИАГНОСТИКУ\n\n💥 СОСТОЯНИЕ НОВОГО АВТОМОБИЛЯ!💥\n\nДилерский центр АУДИ ЦЕНТР ВОСТОК удобно расположен на Востоке Москвы, 2км от МКАД. \n\nНам важно, чтобы при покупке автомобиля Вы чувствовали себя максимально защищенными!\n\n🔁Продайте или обменяйте свой автомобиль на персональных условиях!\n\nОсмотр ежедневно с 9:00 до 21:00, без перерыва и выходных.\nДо встречи в АУДИ ЦЕНТР ВОСТОК!\n\nПТС оригинал.\n\nМесто осмотра\n\nОсмотреть автомобиль можно по адресу: Московская область, Балашиха, ш. Энтузиастов, д. 12Б.\n\nКомплектация «Cayenne Platinum Edition»:\n\nАктивная безопасность:\n— Антиблокировочная система\n— Антипробуксовочная система\n— Система курсовой устойчивости\n— Система помощи при экстренном торможении\n— Датчик давления в шинах\n— ЭРА-ГЛОНАСС\nПассивная безопасность:\n— Подушки безопасности водителя с защитой коленей\n— Подушки безопасности пассажира\n— Боковые передние подушки безопасности\n— Оконные шторки безопасности\n— Блокировка замков задних дверей\n— Система крепления детских автокресел\nПротивоугонная система:\n— Сигнализация с обратной связью\n— Датчик проникновения в салон (датчик объема)\n— Иммобилайзер\n— Центральный замок\nПомощь при вождении:\n— Бортовой компьютер\n— Круиз-контроль\n— Парктроник передний и задний\n— Система помощи при старте в гору\n— Система помощи при спуске с горы\n— Система управления дальним светом\n— Датчик света\n— Датчик дождя\nКомфорт:\n— Активный усилитель руля\n— Запуск двигателя с кнопки\n— Система “старт-стоп”\n— Система доступа без ключа\n— Доводчик дверей\n— Регулировка руля\n— Электрорегулировка сиденья водителя с памятью положения\n— Электрорегулировка сиденья пассажира\n— Электростеклоподъемники передние и задние\n— Электропривод зеркал\n— Электропривод крышки багажника\nУправление климатом и обогрев:\n— Климат-контроль 2-зонный\n— Подогрев сидений водителя и пассажира\n— Подогрев руля\n— Обогрев зеркал\nМультимедиа и навигация:\n— Навигационная система\n— CD\n— USB\n— TV\n— Функция Apple CarPlay\n— Функция Android Auto\n— Голосовое управление\n— Bluetooth\n— Мультифункциональное рулевое колесо\n— Розетка 12V\nСалон и интерьер:\n— Кожаная обивка салона\n— Отделка кожей рычага КПП\n— Кожаный руль\n— Панорамная крыша\n— Спортивные передние сидения\n— Третий задний подголовник\n— Передний центральный подлокотник\n— Подрулевые лепестки переключения передач\n— Накладки на пороги\nЭкстерьер:\n— Размер дисков 21″\n— Тонированные стекла\nОсвещение:\n— Светодиодные фары\n— Адаптивные фары\n— Огни дневного хода\n— Корректор фар\nКомплектность:\n— Отметки ТО Частично\n— ПТС\n— Свидетельство о регистрации\n— 2 комплекта ключей\n— Докатка",
        "year": 2018,
        "generation": "III (2017—2023)",
        "body_type": "Внедорожник",
        "equipment": "Cayenne",
        "modification": "3.0 4WD AT (340 л.с.)",
        "drive_type": "Полный",
        "transmission_type": "Автомат",
        "engine_type": "Бензин",
        "doors_number": 5,
        "color": "Чёрный",
        "pts": "Оригинал",
        "owners_count": "1",
        "mileage": 106406,
        "latitude": 55.796339,
        "longitude": 37.938199
    }

    debug_model = Model()
    pred = asyncio.run(debug_model.predict(car))

    print(f'predicted price - {pred}')
