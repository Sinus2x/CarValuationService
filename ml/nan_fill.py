import pandas as pd


def equipment_typos_transform(equipment: str) -> str:
    """
    Уберем найденные опечатки и приведём колонку к нижнему регистру
    """
    typos_dict = {
        "Bussines": "Business",
        "Elegancе": "Elegance",
        "Premuim": "Premium",
        "Standart": "Standard",
        "70-th Anniversary": "70th Anniversary",
        "Exclusive Mem": "Exclusive Mm",
        "Night Eagle\u200b": "Night Eagle",
        "[BLACK] '22": "[BLACK]'22"
    }
    return typos_dict.get(equipment, equipment).lower()


def fill_equipment(df: pd.DataFrame, models_dict: dict) -> pd.DataFrame:
    def equipment_mode_transform(row, modes_dict):
        if row['equipment'] == 'none':
            return modes_dict.get(
                (row['brand'], row['model'], row['generation']),
                'базовая'
            )
        return row['equipment']

    df.equipment = df.equipment.fillna('none').apply(
        lambda x: equipment_typos_transform(x)
    )

    equipment_modes = models_dict['equipment_modes']
    df['equipment'] = df.apply(
        lambda x: equipment_mode_transform(x, equipment_modes), axis=1
    )
    return df


def fill_na_transform(df: pd.DataFrame, models_dict: dict) -> pd.DataFrame:
    df.description = df.description.fillna('placeholder text')
    df.pts = df.pts.fillna('неизвестно')
    df = fill_equipment(df, models_dict)
    return df


if __name__ == "__main__":
    pass
