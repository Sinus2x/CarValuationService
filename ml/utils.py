import pandas as pd
from ml.nan_fill import fill_na_transform
from ml.add_features import features_extract
from ml.add_text_features import text_features_extract


def feature_transform(car: pd.DataFrame, models_dict: dict) -> pd.DataFrame:
    """

    """
    # Types
    car.sale_end_date = pd.to_datetime(car.sale_end_date)
    # Fill nan
    car = fill_na_transform(car, models_dict)

    # New features extract
    car = features_extract(car, models_dict)

    # Text features extraction:
    # w2v (description, modification, equipment), tf-idf (description)
    car = text_features_extract(car, models_dict)

    return car


if __name__ == "__main__":
    example_car = {
        "brand": "Volkswagen",
        "model": "Passat",
        "sale_end_date": "2023-05-10T12:10:35.878Z",
        "year": 2018,
        "generation": "B8 (2014—2020)",
        "body_type": "Седан",
        "equipment": "",
        "modification": "2.0 TDI DSG (150 л.с.)",
        "color": "Коричневый",
        "owners_count": "2",
        "mileage": 99950,
        "latitude": 54.70739,
        "longitude": 20.507307,
        "crashes": 0,
        "is_taxi": "0",
        "is_carsharing": "0"
    }

    print(feature_transform(pd.Series(example_car).to_frame().T))

