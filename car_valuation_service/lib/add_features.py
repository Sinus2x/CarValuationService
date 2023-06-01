import pandas as pd
import time
import re


def get_city(car: dict, models_dict: dict) -> dict:
    gd = models_dict["geocode_class_instance"]
    car['city'] = gd.query([(car['latitude'], car['longitude'])])[0]['city']
    return car


def get_month(car: dict) -> dict:
    car['month'] = car['sale_end_date'].month
    return car


def get_horse_power(car: dict) -> dict:
    try:
        horse_power = re.search(r'\(.*\)', car['modification']).group()
        horse_power = int(horse_power.strip('( л.с.)'))
    except AttributeError:
        horse_power = 382
    car['horse_power'] = horse_power
    return car


def get_engine_volume(car: dict) -> dict:
    try:
        engine_volume = re.search(r'\d\.\d', car['modification']).group()
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


def get_generation_restyling(car: dict) -> dict:
    def restyling_extract(gen_list: list) -> int:
        """
        Выделяем поколение рестайлинга из списка слов колонки generation
        """
        if len(gen_list) == 4:
            return int(gen_list[-2])
        elif len(gen_list) == 3:
            return 1
        return 0

    generation_split = car['generation'].split()
    car['generation'] = generation_split[0]
    car['generation_years'] = generation_split[-1]
    car['restyling'] = restyling_extract(generation_split)
    return car


def get_mileage_per_year(car: dict) -> dict:
    car['mileage_per_year'] = car['mileage'] / (2023.5 - car['year'])
    return car


def get_concat_feature(car: dict) -> dict:
    car['brand_model_gen_res_mod'] = car['brand'] + ' ' + \
                                    car['model'] + ' ' + \
                                    car['generation'] + ' ' + \
                                    str(car['restyling'])
    return car


def get_base_price(car: dict, models_dict: dict) -> dict:
    def predict_base_price(car, price_grouped):
        result = car.merge(price_grouped, how='left')
        y_pred = result['base_price'].values
        return y_pred

    base_price_grouper_cols = ['brand', 'model', 'generation', 'modification']
    base_price_grouper = models_dict['base_price_grouper']

    car['base_price'] = predict_base_price(pd.Series(car).to_frame().T[base_price_grouper_cols], base_price_grouper)
    return car


def features_extract(car: dict, models_dict: dict) -> dict:
    # city, month, horsepower,
    # engine volume, generation,
    # restyling, mileage per year
    # concat_feature, base price
    time_start = time.time()
    car = get_city(car, models_dict)
    time_city = time.time()
    car = get_month(car)
    time_month = time.time()
    car = get_horse_power(car)
    time_hp = time.time()
    car = get_engine_volume(car)
    time_engine_volume = time.time()
    car = get_generation_restyling(car)
    time_gen_restyling = time.time()
    car = get_mileage_per_year(car)
    time_mileage = time.time()
    car = get_concat_feature(car)
    time_concat = time.time()
    car = get_base_price(car, models_dict)
    time_base_price = time.time()
    print(f"*** features_extract func execution times analysis ***")
    print(f"city extract- {time_city - time_start} seconds")
    print(f"month extract- {time_month - time_city} seconds")
    print(f"horse power extract- {time_hp - time_month} seconds")
    print(f"engine volume extract- {time_engine_volume - time_hp} seconds")
    print(f"generation extract- {time_gen_restyling - time_engine_volume} seconds")
    print(f"mileage per year extract- {time_mileage - time_gen_restyling} seconds")
    print(f"concat feature extract- {time_concat - time_mileage} seconds")
    print(f"base price extract- {time_base_price - time_concat} seconds")
    print(f"*** Sum time for features_extract func - {time_base_price - time_start} seconds")
    print("\n")
    return car


if __name__ == "__main__":
    pass
