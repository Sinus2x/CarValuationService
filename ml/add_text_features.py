import pandas as pd
import numpy as np
import pickle
from gensim.models.callbacks import CallbackAny2Vec
from gensim.models.word2vec import Word2Vec
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from ml.description_lemmatization import lemmatize_description
from gensim.models import KeyedVectors
from pathlib import Path


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


def description_w2v_extract(df: pd.DataFrame) -> pd.DataFrame:
    df = lemmatize_description(df)

    model_save_path = Path(__file__).parent.parent / 'data/weights/desc_w2v_model'
    word_vectors_save_path = Path(__file__).parent.parent / 'data/weights/desc_w2v_word_vectors'

    w2v_model = Word2Vec.load(str(model_save_path))
    w2v_model.wv = KeyedVectors.load(str(word_vectors_save_path), mmap='r')

    desc2vec = Word2VecTransformer(w2v_model=w2v_model)
    w2v_desc_transform = desc2vec.transform(df.lemmatized_description.values)
    cols = [f'w2v_desc_{i}' for i in range(1, 11)]
    w2v_df = pd.DataFrame(w2v_desc_transform, columns=cols)
    df['desc_embs'] = w2v_df.apply(lambda x: cols_to_list(x, cols), axis=1)
    return df


def description_tfidf_extract(df: pd.DataFrame) -> pd.DataFrame:
    model_save_path = Path(__file__).parent.parent / 'data/weights/desc_tfidf_model.pkl'

    with open(model_save_path, 'rb') as f:
        tfidf = pickle.load(f)

    tfidf_df = tfidf.transform(df.lemmatized_description.astype(str).values)
    tfidf_embs_df = pd.DataFrame()
    cols = ['tfidf_sum', 'tfidf_max', 'tfidf_mean']
    tfidf_embs_df['tfidf_sum'] = np.array(tfidf_df.sum(axis=1).ravel())[0]
    tfidf_embs_df['tfidf_max'] = np.array(tfidf_df.max(axis=1).toarray().ravel())
    tfidf_embs_df['tfidf_mean'] = np.array(tfidf_df.mean(axis=1).ravel())[0]
    df['tfidf_embs'] = tfidf_embs_df.apply(lambda x: cols_to_list(x, cols), axis=1)
    return df


def equipment_w2v_extract(df: pd.DataFrame) -> pd.DataFrame:
    model_save_path = Path(__file__).parent.parent / 'data/weights/equip_w2v_model'
    word_vectors_save_path = Path(__file__).parent.parent / 'data/weights/equip_w2v_word_vectors'

    equipment_w2v_model = Word2Vec.load(str(model_save_path))
    equipment_w2v_model.wv = KeyedVectors.load(str(word_vectors_save_path), mmap='r')

    equip_w2v_transformer = Word2VecTransformer(w2v_model=equipment_w2v_model)
    equipment_w2v_df = equip_w2v_transformer.transform(df.equipment.values)
    cols = [f'eq_w2v_{i}' for i in range(1, 6)]
    equipment_w2v_df = pd.DataFrame(equipment_w2v_df, columns=cols)
    df['eq_embs'] = equipment_w2v_df.apply(lambda x: cols_to_list(x, cols), axis=1)
    return df


def modification_w2v_extract(df: pd.DataFrame) -> pd.DataFrame:
    model_save_path = Path(__file__).parent.parent / 'data/weights/modification_w2v_model'
    word_vectors_save_path = Path(__file__).parent.parent / 'data/weights/modification_w2v_word_vectors'

    modification_w2v_model = Word2Vec.load(str(model_save_path))
    modification_w2v_model.wv = KeyedVectors.load(str(word_vectors_save_path), mmap='r')

    modification_w2v_transformer = Word2VecTransformer(w2v_model=modification_w2v_model)
    modification_w2v_df = modification_w2v_transformer.transform(df.modification.values)
    cols = [f'mod_w2v_{i}' for i in range(1, 6)]
    modification_w2v_df = pd.DataFrame(modification_w2v_df, columns=cols)
    df['mod_embs'] = modification_w2v_df.apply(lambda x: cols_to_list(x, cols), axis=1)
    return df


def text_features_extract(df: pd.DataFrame) -> pd.DataFrame:
    # description w2v
    df = description_w2v_extract(df)
    # description tf-idf
    df = description_tfidf_extract(df)
    # equipment w2v
    df = equipment_w2v_extract(df)
    # modification w2v
    df = modification_w2v_extract(df)
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
