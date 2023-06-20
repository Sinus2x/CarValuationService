"""
Модуль, который содержит все функции,
нужные для получения лемматизации текстового описания.
"""

import re
from typing import List


def preprocess_text(description: str) -> List[str]:
    """
    Предобработка и токенизация текста.
    """
    pattern = re.compile(r'[^\W_]+')
    description = pattern.findall(description)
    description = [token.lower() for token in description if len(token) > 1]
    if len(description) == 0:
        return ['placeholder', 'text']
    return description


def lemmatize(description: List[str], models_dict: dict) -> List[str]:
    """
    Лемматизирует токены.
    """
    lemmatizer = models_dict['lemmatizer']
    lemmas = [lemmatizer.parse(word)[0].normal_form for word in description]
    return lemmas


def lemmatize_description(car: dict, models_dict: dict) -> dict:
    """
    Получает готовую лемматизацию текстового описание машины.
    """
    car['description'] = preprocess_text(car['description'])
    car['lemmatized_description_list'] = lemmatize(
        car['description'],
        models_dict
    )
    car['lemmatized_description'] = ' '.join(
        car['lemmatized_description_list']
    )
    return car
