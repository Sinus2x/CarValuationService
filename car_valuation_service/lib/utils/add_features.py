"""
Модуль, который содержит все функции,
нужные для преобразования признаков машины.
"""

import re


def get_city(car: dict, models_dict: dict) -> dict:
    """
    Извлекает город по полям `latitude`, `longitude`.
    """
    geo_decoder = models_dict['geocode_class_instance']
    car['city'] = geo_decoder.query(
        [(car['latitude'], car['longitude'])]
    )[0]['city']
    return car


def get_month(car: dict) -> dict:
    """
    Извлекает месяц по полю `sale_end_date`.
    """
    car['month'] = car['sale_end_date'].month
    return car


def get_horse_power(car: dict) -> dict:
    """
    Извлекает регулярным выражением
     лошадиные силы двигателя из поля `modification`.
     """
    try:
        pattern = re.compile(r'\(.*\)')
        horse_power = pattern.search(car['modification']).group()
        horse_power = int(horse_power.strip('( л.с.)'))
    except AttributeError:
        horse_power = 382
    car['horse_power'] = horse_power
    return car


def get_engine_volume(car: dict) -> dict:
    """
    Извлекает регулярным выражением
     объём цилиндров двигателя из поля `modification`.
     """
    try:
        pattern = re.compile(r'\d\.\d')
        engine_volume = pattern.search(car['modification']).group()
    except AttributeError:
        if car['modification'] == 'FX30d 4WD AT (238 л.с.)':
            engine_volume = '3.0'
        elif car['modification'] == 'P85':
            engine_volume = '0.0'
        elif car['model'] == 'FX30':
            engine_volume = '3.0'
        else:
            engine_volume = '2.4'
    car['engine_volume'] = engine_volume
    return car


def restyling_extract(gen_list: list) -> int:
    """
    Выделяем поколение рестайлинга из списка слов поля `generation`.
    """
    if len(gen_list) == 4:
        return int(gen_list[-2])
    if len(gen_list) == 3:
        return 1
    return 0


def get_generation_restyling(car: dict) -> dict:
    """
    Извлекает признаки поколения и рестайлинга из поля `generation`.
    """
    generation_split = car['generation'].split()
    car['generation'] = generation_split[0]
    car['generation_years'] = generation_split[-1]
    car['restyling'] = restyling_extract(generation_split)
    return car


def get_mileage_per_year(car: dict, models_dict: dict) -> dict:
    """
    Вычисляет пробег в год по полям `mileage`, `year`.
    """
    car['mileage_per_year'] = car['mileage'] / (
            models_dict['cur_year'] - car['year']
    )
    return car


def get_concat_feature(car: dict) -> dict:
    """
    Получаем длинную строку из полей
    `brand`, `model`, `generation`, `restyling`.
    """
    keys = ['brand', 'model', 'generation']
    car['brand_model_gen_res_mod'] = ' '.join(
        car[key] for key in keys) + str(car['restyling'])
    return car


def get_base_price(car: dict, models_dict: dict) -> dict:
    """
    Получаем базовую цену по группе полей,
    используя класс `BasePriceGrouper`.
    """
    base_price_grouper = models_dict['base_price_grouper']
    car['base_price'] = base_price_grouper.predict(car)
    return car


def features_extract(car: dict, models_dict: dict) -> dict:
    """
    Извлекает и добавляет признаки машины, нужные для модели.

    Список новых признаков:
    - `city`
    - `month`
    - `horsepower`
    - `engine_volume`
    - `restyling`
    - `mileage_per_year`
    - и т.п.
    """
    features = [
        get_month,
        get_horse_power,
        get_engine_volume,
        get_generation_restyling,
        get_concat_feature,
    ]
    for get_feature in features:
        car = get_feature(car)
    car = get_city(car, models_dict)
    car = get_base_price(car, models_dict)
    car = get_mileage_per_year(car, models_dict)
    return car
