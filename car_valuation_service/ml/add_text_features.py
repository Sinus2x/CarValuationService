import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from ml.description_lemmatization import lemmatize_description
import time


class Word2VecTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, w2v_model, alpha=1):
        self.w2v_model = w2v_model
        self.alpha = alpha

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X_transformed = np.zeros((len(X), self.w2v_model.wv.vector_size))
        for i, title in enumerate(X):
            title_vector = np.zeros((self.w2v_model.wv.vector_size,))
            try:
                tokens = title.split()
            except BaseException:
                continue
            counter = 1

            for token in tokens:
                if token in self.w2v_model.wv.key_to_index:
                    title_vector += self.w2v_model.wv.get_vector(token)
                    counter += 1
            X_transformed[i] = title_vector / (self.alpha * counter)

        return X_transformed


def cols_to_list(row, cols):
    lst = []
    for col in cols:
        lst.append(row[col])
    return lst


def description_w2v_extract(df: pd.DataFrame, models_dict: dict) -> pd.DataFrame:
    time_lemm_start = time.time()
    df = lemmatize_description(df, models_dict)
    time_lemm_end = time.time()

    w2v_model = models_dict['w2v_model']
    w2v_model.wv = models_dict['w2v_model_wv']

    desc2vec = Word2VecTransformer(w2v_model=w2v_model)
    w2v_desc_transform = desc2vec.transform(df.lemmatized_description.values)
    cols = [f'w2v_desc_{i}' for i in range(1, 11)]
    w2v_df = pd.DataFrame(w2v_desc_transform, columns=cols)
    df['desc_embs'] = w2v_df.apply(lambda x: cols_to_list(x, cols), axis=1)
    time_desc_w2v_tranform_end = time.time()
    print(f"****** desc_w2v_extract func analysis ******")
    print(f"lemmatization - {time_lemm_end - time_lemm_start} seconds")
    print(f"tranform - {time_desc_w2v_tranform_end - time_lemm_end} seconds")
    print("************")
    return df


def description_tfidf_extract(df: pd.DataFrame, models_dict: dict) -> pd.DataFrame:
    tfidf = models_dict['tfidf']
    tfidf_df = tfidf.transform(df.lemmatized_description.astype(str).values)
    tfidf_embs_df = pd.DataFrame()
    cols = ['tfidf_sum', 'tfidf_max', 'tfidf_mean']
    tfidf_embs_df['tfidf_sum'] = np.array(tfidf_df.sum(axis=1).ravel())[0]
    tfidf_embs_df['tfidf_max'] = np.array(tfidf_df.max(axis=1).toarray().ravel())
    tfidf_embs_df['tfidf_mean'] = np.array(tfidf_df.mean(axis=1).ravel())[0]
    df['tfidf_embs'] = tfidf_embs_df.apply(lambda x: cols_to_list(x, cols), axis=1)
    return df


def equipment_w2v_extract(df: pd.DataFrame, models_dict: dict) -> pd.DataFrame:
    equipment_w2v_model = models_dict['eq_w2v_model']
    equipment_w2v_model.wv = models_dict['eq_w2v_model_wv']
    equip_w2v_transformer = Word2VecTransformer(w2v_model=equipment_w2v_model)
    equipment_w2v_df = equip_w2v_transformer.transform(df.equipment.values)
    cols = [f'eq_w2v_{i}' for i in range(1, 6)]
    equipment_w2v_df = pd.DataFrame(equipment_w2v_df, columns=cols)
    df['eq_embs'] = equipment_w2v_df.apply(lambda x: cols_to_list(x, cols), axis=1)
    return df


def modification_w2v_extract(df: pd.DataFrame, models_dict: dict) -> pd.DataFrame:
    modification_w2v_model = models_dict['mod_w2v_model']
    modification_w2v_model.wv = models_dict['mod_w2v_model_wv']
    modification_w2v_transformer = Word2VecTransformer(w2v_model=modification_w2v_model)
    modification_w2v_df = modification_w2v_transformer.transform(df.modification.values)
    cols = [f'mod_w2v_{i}' for i in range(1, 6)]
    modification_w2v_df = pd.DataFrame(modification_w2v_df, columns=cols)
    df['mod_embs'] = modification_w2v_df.apply(lambda x: cols_to_list(x, cols), axis=1)
    return df


def text_features_extract(df: pd.DataFrame, models_dict: dict) -> pd.DataFrame:
    time_start = time.time()
    # description w2v
    df = description_w2v_extract(df, models_dict)
    time_desc_w2v = time.time()
    # description tf-idf
    df = description_tfidf_extract(df, models_dict)
    time_desc_tfidf = time.time()
    # equipment w2v
    df = equipment_w2v_extract(df, models_dict)
    time_eq_w2v = time.time()
    # modification w2v
    df = modification_w2v_extract(df, models_dict)
    time_mod_w2v = time.time()

    print(f"*** text_features_extract func execution times analysis ***")
    print(f"desc w2v extract- {time_desc_w2v - time_start} seconds")
    print(f"desc tfidf extract- {time_desc_tfidf - time_desc_w2v} seconds")
    print(f"equipment w2v extract- {time_eq_w2v - time_desc_tfidf} seconds")
    print(f"modification w2v extract- {time_mod_w2v - time_eq_w2v} seconds")
    print(f"*** Sum time for text_features_extract func - {time_mod_w2v - time_start} seconds")
    print("\n")
    return df


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
