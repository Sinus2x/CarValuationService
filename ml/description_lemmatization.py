import pandas as pd
import numpy as np
import re
from pymystem3 import Mystem


def preprocess_text(text):
    text = re.findall('[^\W_]+', text)
    text = [token.lower() for token in text if len(token) > 1]
    text = " ".join(text)
    if len(text) == 0:
        return 'placeholder text'
    return text


def lemmatize(text):
    m = Mystem()
    lemmas = m.lemmatize(text)
    return ''.join(lemmas)


def lemmatize_description(df: pd.DataFrame) -> pd.DataFrame:
    df['description'] = df.description.apply(preprocess_text)
    df['lemmatized_description'] = df.description.apply(lemmatize)
    #print(df['lemmatized_description'])
    return df


if __name__ == "__main__":
    pass
