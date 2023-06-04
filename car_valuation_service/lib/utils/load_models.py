"""
Модуль для загрузки всех моделей и весов,
необходимых для обработки и предсказания цены
"""


import pickle
from datetime import datetime
from pathlib import Path
from gensim.models.word2vec import Word2Vec
from gensim.models import KeyedVectors
from reverse_geocode import GeocodeData
from pymorphy2 import MorphAnalyzer
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np
import yaml
from lib.utils.base_price_grouper import BasePriceGrouper


CONFIG_DIR = Path(__file__).parent.parent
ROOT_DIR = Path(__file__).parent.parent.parent
CONFIG_PATH = CONFIG_DIR / "config.yaml"
with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
    CONFIG = yaml.load(config_file, Loader=yaml.FullLoader)


class Word2VecTransformer(BaseEstimator, TransformerMixin):
    """
    Класс трансформера для получения эмбеддингов текстовых признаков
    из эмбеддингов отдельных слов, полученных с помощью Word2Vec
    """
    def __init__(self, w2v_model, alpha=1):
        """
        Конструктор класса
        """
        self.w2v_model = w2v_model
        self.alpha = alpha

    def transform(self, tokens):
        """
        Метод класса, преобразующий эмбеддинги токенов
        в эмбеддинг набора токенов - текста.
        """
        token_vectors = np.zeros((self.w2v_model.wv.vector_size,))
        counter = 1
        for token in tokens:
            if token in self.w2v_model.wv.key_to_index:
                token_vectors += self.w2v_model.wv.get_vector(token)
                counter += 1
        text_vector = token_vectors / (self.alpha * counter)
        return text_vector


def load_models() -> dict:
    """
    Функция загрузки классов, весов и .csv,
    необходимых для преобразования входных признаков и
    выделения новых для их последующей передачи в
    функцию предсказания цены.

    Загруженные объекты передаются далее с помощью словаря.
    """
    geocode_class_instance = GeocodeData()

    lemmatizer = MorphAnalyzer()

    equipment_modes = pd.read_csv(ROOT_DIR / CONFIG["equipment_path"])

    df_groups = pd.read_csv(ROOT_DIR / CONFIG["base_price_path"])
    base_price_grouper = BasePriceGrouper(df_groups)

    w2v_model = Word2Vec.load(str(ROOT_DIR / CONFIG["desc_w2v_path"]))
    w2v_model.wv = KeyedVectors.load(
        str(ROOT_DIR / CONFIG["desc_w2v_vectors_path"]),
        mmap="r"
    )
    desc2vec = Word2VecTransformer(w2v_model=w2v_model)

    with open(ROOT_DIR / CONFIG["desc_tfidf_path"], "rb") as tfidf_model:
        tfidf = pickle.load(tfidf_model)

    equipment_w2v_model = Word2Vec.load(
        str(ROOT_DIR / CONFIG["equip_w2v_path"])
    )
    equipment_w2v_model.wv = KeyedVectors.load(
        str(ROOT_DIR / CONFIG["equip_w2v_vectors_path"]),
        mmap="r"
    )
    eq2vec = Word2VecTransformer(w2v_model=equipment_w2v_model)

    modification_w2v_model = Word2Vec.load(
        str(ROOT_DIR / CONFIG["mod_w2v_path"])
    )
    modification_w2v_model.wv = KeyedVectors.load(
        str(ROOT_DIR / CONFIG["mod_w2v_vectors_path"]),
        mmap="r"
    )
    mod2vec = Word2VecTransformer(w2v_model=modification_w2v_model)

    cur_year = datetime.now().year + ((datetime.now().month - 1) / 12)

    features_models_dict = {
        "geocode_class_instance": geocode_class_instance,
        "lemmatizer": lemmatizer,
        "base_price_grouper": base_price_grouper,
        "equipment_modes": equipment_modes,
        "desc2vec": desc2vec,
        "tfidf": tfidf,
        "eq2vec": eq2vec,
        "mod2vec": mod2vec,
        "cur_year": cur_year
    }

    return features_models_dict
