import pandas as pd
import numpy as np
from lib.description_lemmatization import lemmatize_description
import time


def cols_to_list(row, cols):
    lst = []
    for col in cols:
        lst.append(row[col])
    return lst


def description_w2v_extract(car: dict, models_dict: dict) -> dict:
    time_lemm_start = time.time()
    car = lemmatize_description(car, models_dict)
    time_lemm_end = time.time()
    desc2vec = models_dict["desc2vec"]
    w2v_desc_transform = desc2vec.transform(car['lemmatized_description_list'])
    car['desc_embs'] = w2v_desc_transform
    time_desc_w2v_tranform_end = time.time()
    print(f"****** desc_w2v_extract func analysis ******")
    print(f"lemmatization - {time_lemm_end - time_lemm_start} seconds")
    print(f"transform - {time_desc_w2v_tranform_end - time_lemm_end} seconds")
    print("************")
    return car


def description_tfidf_extract(car: dict, models_dict: dict) -> dict:
    tfidf = models_dict['tfidf']
    tfidf_df = tfidf.transform([car['lemmatized_description']])
    car['tfidf_embs'] = [
        tfidf_df.sum(),
        tfidf_df.max(),
        tfidf_df.mean()
    ]
    return car


def equipment_w2v_extract(car: dict, models_dict: dict) -> dict:
    equip_w2v_transformer = models_dict["eq2vec"]
    equipment_w2v_df = equip_w2v_transformer.transform(car['equipment'].split())
    car['eq_embs'] = equipment_w2v_df
    return car


def modification_w2v_extract(car: dict, models_dict: dict) -> dict:
    modification_w2v_transformer = models_dict["mod2vec"]
    modification_w2v_df = modification_w2v_transformer.transform(car['modification'].split())
    car['mod_embs'] = modification_w2v_df
    return car


def text_features_extract(car: dict, models_dict: dict) -> dict:
    time_start = time.time()
    # description w2v
    car = description_w2v_extract(car, models_dict)
    time_desc_w2v = time.time()
    # description tf-idf
    car = description_tfidf_extract(car, models_dict)
    time_desc_tfidf = time.time()
    # equipment w2v
    car = equipment_w2v_extract(car, models_dict)
    time_eq_w2v = time.time()
    # modification w2v
    car = modification_w2v_extract(car, models_dict)
    time_mod_w2v = time.time()
    print(f"*** text_features_extract func execution times analysis ***")
    print(f"desc w2v extract- {time_desc_w2v - time_start} seconds")
    print(f"desc tfidf extract- {time_desc_tfidf - time_desc_w2v} seconds")
    print(f"equipment w2v extract- {time_eq_w2v - time_desc_tfidf} seconds")
    print(f"modification w2v extract- {time_mod_w2v - time_eq_w2v} seconds")
    print(f"*** Sum time for text_features_extract func - {time_mod_w2v - time_start} seconds")
    print("\n")
    return car


if __name__ == "__main__":
    df_cols = [
        'actual_price', 'price', 'start_date',
        'close_date', 'sale_end_date', 'brand',
        'model', 'generation', 'modification',
        'equipment', 'body_type', 'drive_type',
        'transmission_type', 'engine_type', 'doors_number',
        'color', 'pts', 'year', 'mileage', 'owners_count',
        'latitude', 'longitude', 'description',
    ]

    df_to_transform = pd.read_feather(
        'project_train.f',
        columns=df_cols
    )

    #head_1 = description_tfidf_extract(fill_na_transform(df_to_transform), use_pretrained=True)
    #head_2 = description_w2v_extract(df_to_transform, use_pretrained=True).head()

    #print(head_1.head())
    #print('*'*10)
    #print(head_1.isna().sum())

    #print(lemmatize_description(df_to_transform).info())
