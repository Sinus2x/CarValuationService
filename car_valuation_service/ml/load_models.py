from gensim.models.word2vec import Word2Vec
from gensim.models import KeyedVectors
from pathlib import Path
from reverse_geocode import GeocodeData
from pymorphy2 import MorphAnalyzer
import pandas as pd
import numpy as np
import pickle
from sklearn.base import BaseEstimator, TransformerMixin


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


def load_models() -> dict:
    # geocode class init
    geocode_class_instance = GeocodeData()

    # lemmatizer init
    lemmatizer = MorphAnalyzer()

    # equipment modes
    modes_path = Path(__file__).parent.parent / "data/weights/equipment_modes.csv"
    equipment_modes = pd.read_csv(modes_path)

    # base_price_grouper
    grouper_path = Path(__file__).parent.parent / "data/weights/base_price_grouper.csv"
    base_price_grouper = pd.read_csv(grouper_path)

    # desc w2v
    model_save_path = Path(__file__).parent.parent / 'data/weights/desc_w2v_model'
    word_vectors_save_path = Path(__file__).parent.parent / 'data/weights/desc_w2v_word_vectors'
    w2v_model = Word2Vec.load(str(model_save_path))
    w2v_model.wv = KeyedVectors.load(str(word_vectors_save_path), mmap='r')
    desc2vec = Word2VecTransformer(w2v_model=w2v_model)

    # desc tf-idf
    model_save_path = Path(__file__).parent.parent / 'data/weights/desc_tfidf_model.pkl'
    with open(model_save_path, 'rb') as f:
        tfidf = pickle.load(f)

    # eq w2v
    model_save_path = Path(__file__).parent.parent / 'data/weights/equip_w2v_model'
    word_vectors_save_path = Path(__file__).parent.parent / 'data/weights/equip_w2v_word_vectors'
    equipment_w2v_model = Word2Vec.load(str(model_save_path))
    equipment_w2v_model.wv = KeyedVectors.load(str(word_vectors_save_path), mmap='r')
    eq2vec = Word2VecTransformer(w2v_model=equipment_w2v_model)

    # mod w2v
    model_save_path = Path(__file__).parent.parent / 'data/weights/modification_w2v_model'
    word_vectors_save_path = Path(__file__).parent.parent / 'data/weights/modification_w2v_word_vectors'
    modification_w2v_model = Word2Vec.load(str(model_save_path))
    modification_w2v_model.wv = KeyedVectors.load(str(word_vectors_save_path), mmap='r')
    mod2vec = Word2VecTransformer(w2v_model=modification_w2v_model)

    features_models_dict = {
        "geocode_class_instance": geocode_class_instance,
        "lemmatizer": lemmatizer,
        "base_price_grouper": base_price_grouper,
        "equipment_modes": equipment_modes,
        "desc2vec": desc2vec,
        "tfidf": tfidf,
        "eq2vec": eq2vec,
        "mod2vec": mod2vec
    }

    return features_models_dict


if __name__ == "__main__":
    pass
