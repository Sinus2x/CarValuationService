"""
Модуль, который содержит все функции,
нужные для получения текстовых признаков.
"""

from lib.utils.description_lemmatization import lemmatize_description


def cols_to_list(row, cols):
    """
    Преобразует колонки в лист.
    """
    lst = []
    for col in cols:
        lst.append(row[col])
    return lst


def description_w2v_extract(car: dict, models_dict: dict) -> dict:
    """
    Получает word2vec эмбеддинги лемматизированного описания.
    """
    car = lemmatize_description(car, models_dict)
    desc2vec = models_dict["desc2vec"]
    w2v_desc_transform = desc2vec.transform(car['lemmatized_description_list'])
    car['desc_embs'] = w2v_desc_transform
    return car


def description_tfidf_extract(car: dict, models_dict: dict) -> dict:
    """
    Получает tf-idf для лемматизированного описания.
    """
    tfidf = models_dict['tfidf']
    tfidf_df = tfidf.transform([car['lemmatized_description']])
    car['tfidf_embs'] = [
        tfidf_df.sum(),
        tfidf_df.max(),
        tfidf_df.mean()
    ]
    return car


def equipment_w2v_extract(car: dict, models_dict: dict) -> dict:
    """
    Получает word2vec эмбеддинги оборудования машины.
    """
    equip_w2v_transformer = models_dict["eq2vec"]
    equipment_w2v_df = equip_w2v_transformer.transform(
        car['equipment'].split()
    )
    car['eq_embs'] = equipment_w2v_df
    return car


def modification_w2v_extract(car: dict, models_dict: dict) -> dict:
    """
    Получает word2vec эмбеддинги модификации двигателя.
    """
    modification_w2v_transformer = models_dict["mod2vec"]
    modification_w2v_df = modification_w2v_transformer.transform(
        car['modification'].split()
    )
    car['mod_embs'] = modification_w2v_df
    return car


def text_features_extract(car: dict, models_dict: dict) -> dict:
    """
    Получает все текстовые признаки.

    - word2vec эмбеддинги описания
    - tf-idf для описания
    - word2vec эмбеддинги оборудования машины
    - word2vec эмбеддинги модификации двигателя
    """

    text_features = [
        description_w2v_extract,
        description_tfidf_extract,
        equipment_w2v_extract,
        modification_w2v_extract,
    ]
    for get_text_feature in text_features:
        car = get_text_feature(car, models_dict)
    return car
