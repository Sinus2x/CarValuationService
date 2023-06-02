"""
Модуль, который содержит все функции для
заполнения пропусков в данных.
"""


def equipment_typos_transform(equipment: str) -> str:
    """
    Уберем найденные опечатки и
    приведём колонку к нижнему регистру.
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


def equipment_mode_transform(row, modes_dict):
    """
    Заполняет пропуск в поле `equipment` по умолчанию.
    """
    if row['equipment'] == 'none':
        return modes_dict.get(
            (row['brand'], row['model'], row['generation']),
            'базовая'
        )
    return row['equipment']


def fill_equipment(car: dict, models_dict: dict) -> dict:
    """
    Заполняет пропуски и опечатки в поле `equipment`.
    """
    car['equipment'] = equipment_typos_transform(car['equipment'])
    equipment_modes = models_dict['equipment_modes']
    car['equipment'] = equipment_mode_transform(car, equipment_modes)
    return car


def fill_na_transform(car: dict, models_dict: dict) -> dict:
    """
    Заполняет пропуски и опечатки в тексте, в полях `pts` и `equipment`.
    """
    if not car["description"]:
        car["description"] = 'placeholder text'
    if not car["pts"]:
        car["pts"] = 'неизвестно'

    car = fill_equipment(car, models_dict)
    return car
