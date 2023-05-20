import pandas as pd
import reverse_geocode


def get_city(df: pd.DataFrame, drop_coord_cols: bool = True) -> pd.DataFrame:
    cities = reverse_geocode.search(df[['latitude', 'longitude']].values)
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
    df = get_city(df)
    df = get_month(df)
    df = get_horse_power(df)
    df = get_engine_volume(df)
    df = get_generation_restyling(df)
    df = get_mileage_per_year(df)
    df = get_concat_feature(df)
    df = get_base_price(df, models_dict)
    return df


if __name__ == "__main__":
    """from pathlib import Path
    car = {
    "brand": "Porsche",
    "model": "Cayenne",
    "generation": "III (2017—2023)",
    "modification": "3.0 4WD AT (340 л.с.)",
    }

    car = pd.Series(car).to_frame().T

    weights_save_path = "data/weights/base_price_grouper.csv"
    path = Path(__file__).parent.parent / weights_save_path
    base_price_grouper = pd.read_csv(path)

    features_models_dict = {
        "base_price_grouper": base_price_grouper,}

    car = get_base_price(car, features_models_dict)
    print(car)"""
    pass
