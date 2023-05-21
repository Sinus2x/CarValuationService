import pandas as pd
import time


def get_city(df: pd.DataFrame, models_dict: dict, drop_coord_cols: bool = True) -> pd.DataFrame:
    gd = models_dict["geocode_class_instance"]
    cities = gd.query(df[['latitude', 'longitude']].values)
    df['city'] = [i['city'] for i in cities]
    if drop_coord_cols:
        df = df.drop(['latitude', 'longitude'], axis=1)
    return df


def get_month(df: pd.DataFrame) -> pd.DataFrame:
    def month_extract(row):
        if row['sale_end_date'] is pd.NaT:
            return row['close_date'].month
        return row['sale_end_date'].month

    df['month'] = df.apply(lambda x: month_extract(x), axis=1)
    return df


def get_horse_power(df: pd.DataFrame) -> pd.DataFrame:
    hp_df = df.modification.str.extract(r'(?P<horse_power>\(.*\))')
    horse_power = hp_df.horse_power.str.strip('( л.с.)').fillna('382')
    horse_power = horse_power.astype(int)
    df['horse_power'] = horse_power
    return df


def get_engine_volume(df: pd.DataFrame) -> pd.DataFrame:
    tmp_df = df[['modification', 'model']]
    tmp_df['engine_volume'] = tmp_df.modification.str.extract(r'(?P<engine_volume>\d\.\d)')
    tmp_df.loc[tmp_df['modification'] == 'FX30d 4WD AT (238 л.с.)', 'engine_volume'] = '3.0'
    tmp_df.loc[tmp_df['modification'] == 'P85', 'engine_volume'] = '0.0'
    tmp_df.loc[tmp_df['model'] == 'FX30', 'engine_volume'] = '3.0'
    df['engine_volume'] = tmp_df['engine_volume']
    return df


def get_generation_restyling(df: pd.DataFrame) -> pd.DataFrame:
    def restyling_extract(gen_list: list) -> int:
        """
        Выделяем поколение рестайлинга из списка слов колонки generation
        """
        if len(gen_list) == 4:
            return int(gen_list[-2])
        elif len(gen_list) == 3:
            return 1
        return 0

    generation_split = df['generation'].str.split()
    df['generation'] = generation_split.apply(lambda x: x[0])
    df['generation_years'] = generation_split.apply(lambda x: x[-1])
    df['restyling'] = generation_split.apply(lambda x: restyling_extract(x))
    return df


def get_mileage_per_year(df: pd.DataFrame) -> pd.DataFrame:
    df['mileage_per_year'] = df.mileage / (
            df.year.max() +
            (
                    df[df.year.eq(df.year.max())].month.max() / 12
            ) - df.year
    )
    return df


def get_concat_feature(df: pd.DataFrame) -> pd.DataFrame:
    df['brand_model_gen_res_mod'] = df.brand + ' ' + \
                                    df.model + ' ' + \
                                    df.generation + ' ' + \
                                    df.restyling.astype(str)
    return df


def get_base_price(df: pd.DataFrame, models_dict: dict) -> pd.DataFrame:
    def predict_base_price(X, price_grouped):
        result = X.merge(price_grouped, how='left')
        y_pred = result['base_price'].values
        return y_pred

    base_price_grouper_cols = ['brand', 'model', 'generation', 'modification']
    base_price_grouper = models_dict['base_price_grouper']
    df['base_price'] = predict_base_price(df[base_price_grouper_cols], base_price_grouper)
    return df


def features_extract(df: pd.DataFrame, models_dict: dict) -> pd.DataFrame:
    # city, month, horsepower,
    # engine volume, generation,
    # restyling, mileage per year
    # concat_feature, base price
    time_start = time.time()
    df = get_city(df, models_dict)
    time_city = time.time()
    df = get_month(df)
    time_month = time.time()
    df = get_horse_power(df)
    time_hp = time.time()
    df = get_engine_volume(df)
    time_engine_volume = time.time()
    df = get_generation_restyling(df)
    time_gen_restyling = time.time()
    df = get_mileage_per_year(df)
    time_mileage = time.time()
    df = get_concat_feature(df)
    time_concat = time.time()
    df = get_base_price(df, models_dict)
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
    return df


if __name__ == "__main__":
    pass
