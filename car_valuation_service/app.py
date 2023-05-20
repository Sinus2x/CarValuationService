import os
import time
from fastapi import FastAPI
from pydantic import BaseModel
from ml.datatypes import Car
from load_models import load_model
from logging import getLogger
from statsd import StatsClient


logger = getLogger()

GRAPHITE_HOST = os.environ.get('GRAPHITE_HOST', None)
GRAPHITE_PORT = os.environ.get('GRAPHITE_PORT', None)
logger.warning(f'graphite url: {GRAPHITE_HOST}, port: {GRAPHITE_PORT}')
statsd = StatsClient(GRAPHITE_HOST, int(GRAPHITE_PORT), prefix='car_valuation_service')


class Prediction(BaseModel):
    predicted_value: int


model = None
app = FastAPI()


# create a route
@app.get("/")
def index():
    return {"text": "Welcome to Car Valuation Service!"}


# Register the function to run during startup
@app.on_event("startup")
def startup_event():
    global model
    model = load_model()


@app.post("/predict")
def predict(x: Car):
    time_start = time.perf_counter()
    pred = model.predict(x.dict())
    time_end = time.perf_counter()
    statsd.timing(f'predict_price.timing.inference_time', time_end - time_start)
    statsd.incr(f'predict_price.request_status.success.count')
    return Prediction(
        predicted_value=int(pred)
    )


if __name__ == "__main__":
    pass
