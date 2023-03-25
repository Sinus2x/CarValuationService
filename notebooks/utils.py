import os

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from scipy.stats import entropy

from IPython.core.display import HTML


class MultiCatManager():
    def __init__(self, train_df: pd.DataFrame, test_df: pd.DataFrame, multicats: list, name: str) -> None:
        self.train_df = train_df
        self.test_df = test_df
        self.multicats = multicats
        self.name = name
        self.cv_dict = {}

    def build(self) -> None:
        for multicat in self.multicats:
            values = pd.unique(np.concatenate([self.train_df[multicat].unique(), self.test_df[multicat].unique()]))
            cv = CountVectorizer(preprocessor=lambda x: str(x).strip('[]'), tokenizer=lambda x: x.replace(', ', ',').split(','))
            cv.fit(values)
            self.cv_dict[multicat] = cv

    def get_entropy(self, df: pd.DataFrame) -> list:
        result = []
        for multicat in self.multicats:
            cv = self.cv_dict[multicat]
            transformed = cv.transform(df[multicat].values).toarray()
            _, counts = np.unique(transformed, return_counts=True, axis=0)
            result.append(entropy(counts, base=2))

        return result

    def get_variance(self, df: pd.DataFrame, column: str) -> list:
        result = []

        def sum_of_sqrs(arr):
            mean = arr.mean()
            return ((arr - mean) ** 2).sum()

        for multicat in self.multicats:
            cv = self.cv_dict[multicat]
            transformed = cv.transform(df[multicat].values).toarray()
            transformed = np.apply_along_axis(str, axis=1, arr=transformed)
            temp_df = pd.DataFrame()
            temp_df[multicat] = transformed
            temp_df[column] = df[column].values

            all_var = sum_of_sqrs(df[column].values)
            agg = pd.pivot_table(temp_df, index=multicat, aggfunc=[sum_of_sqrs])
            cat_sum_of_var_sqd = agg[agg.columns[0]].sum()
            r2 = 1 - (cat_sum_of_var_sqd /all_var )
            result.append(r2)

        return result


def get_multicat_info(values: np.array, column: str, dfs: list, names: list, options: pd.DataFrame):
    cv = CountVectorizer(preprocessor=lambda x: str(x).strip('[]'), tokenizer=lambda x: x.replace(', ', ',').split(','))
    X = values
    cv.fit(X)

    index = np.unique(cv.transform(X).toarray(), axis=0)
    index = sorted(index, key=lambda x: sum(x) + np.dot(np.array(x), 2 ** np.arange(len(x))) * 1e-8)
    index = cv.inverse_transform(index)

    flag = False
    for row in index:
        for idx in row:
            if idx.isnumeric():
                flag = True
                break
        else:
            continue
        break
    if flag:
        options_index = list(map(lambda row: list(map(lambda x: options.loc[int(x)].item() if x.isnumeric() else x, row)), index))
        options_index = list(map(lambda x: ', '.join(x), options_index))

    index = list(map(lambda x: ', '.join(x), index))
    result_info = pd.DataFrame(index=options_index if flag else index)

    for data, name in zip(dfs, names):
        multicat_info = pd.DataFrame(columns=['total', 'percentage', 'multi total', 'multi percentage'], index=options_index if flag else index)
        transformed_column = cv.transform(data[column]).toarray()
        n = data.shape[0]
        for idx, multicat in enumerate(index):
            transformed_multicat = cv.transform([multicat]).toarray()[0]
            total = (transformed_column == transformed_multicat).all(axis=1).sum()
            percentage = total / n
            multi_total = ((transformed_column - transformed_multicat) != -1).all(axis=1).sum()
            multi_percentage = multi_total / n
            multicat_info.loc[options_index[idx] if flag else multicat] = [total, np.round(percentage * 100, 4), multi_total, np.round(multi_percentage * 100, 4)]

        multicat_info.columns = pd.MultiIndex.from_product([[name], multicat_info.columns])
        result_info = pd.concat([result_info, multicat_info], axis=1)

    result_info.columns = pd.MultiIndex.from_tuples(result_info.columns)
    return result_info.drop(['total', 'multi total'], axis=1, level=1)


def generate_widget_html(filename: str, feature_names: list, train_df, dealer_df, advert_df, test_df, options):
    dict_info = {}
    out = []

    for name in feature_names:
        X = pd.unique(np.concatenate([train_df[name].unique(), test_df[name].unique()]))
        dict_info[name] = get_multicat_info(X, name, dfs=[train_df, dealer_df, advert_df, test_df], names=['train_df', 'dealer_df', 'advert_df', 'test_df'], options=options)
        template = f"<details><summary>{name}</summary>{dict_info[name].to_html()}</details>"
        out.append(template)

    with open(f'{filename}.html', 'w') as file:
        file.write(''.join(out))

    # display(accordion)


def get_widget_html(filename: str, feature_names: list, train_df, dealer_df, advert_df, test_df, options):
    if not os.path.isfile(f'./{filename}.html'):
        generate_widget_html(filename, feature_names, train_df, dealer_df, advert_df, test_df, options)
    return HTML(filename=f'./{filename}.html')
