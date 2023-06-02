"""
Модуль сервиса предсказания цены автомобиля.

С помощью ручки /predict можно послать POST запрос с JSONом
признаков автомобиля и получить предсказание его цены.
"""


import os
import time
from logging import getLogger
from fastapi import FastAPI
from statsd import StatsClient
from lib.datatypes import Car, Prediction
from lib.model import Model


logger = getLogger()
model = Model()
app = FastAPI()

GRAPHITE_HOST = os.environ.get('GRAPHITE_HOST', None)
GRAPHITE_PORT = os.environ.get('GRAPHITE_PORT', None)
logger.warning(f'graphite url: {GRAPHITE_HOST}, port: {GRAPHITE_PORT}')
statsd = StatsClient(
    GRAPHITE_HOST,
    int(GRAPHITE_PORT),
    prefix='car_valuation_service'
)


@app.get("/")
def index():
    """
    Index handler
    """
    return {"text": "Welcome to Car Valuation Service!"}


@app.post("/predict")
async def predict(car: Car) -> Prediction:
    """
    Ручка предсказания цены

    С помощью метода POST передаётся JSON с
    признаками автомобиля и возвращается
    предсказанная цена автомобиля.

    Statsd собирает данные (count, request status и timings) и
    симулирует ошибку для мониторинга и демонстрации.
    """
    statsd.incr('predict_price.count')
    error_brands = {
        'CheryExeed', 'Dongfeng', 'EXEED', 'GMC',
        'Haima', 'Isuzu', 'JMC', 'Saturn', 'Tianye', 'ЗИЛ'
    }
    if car.brand in error_brands:
        statsd.incr('predict_price.request_status.error.count')
        raise KeyError

    time_start = time.perf_counter()
    prediction = await model.predict(car.dict())
    time_end = time.perf_counter()
    statsd.timing(
        'predict_price.timing.inference_time',
        time_end - time_start
    )
    statsd.incr('predict_price.request_status.success.count')

    return Prediction(predicted_price=prediction)
