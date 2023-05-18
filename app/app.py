from fastapi import FastAPI
from pydantic import BaseModel
from ml.datatypes import Car
from ml.model import Model

model = None
app = FastAPI()


# create a route
@app.get("/")
def index():
    return {"text": "Sentiment Analysis"}


# Register the function to run during startup
@app.on_event("startup")
def startup_event():
    global model
    model = Model()


@app.post("/predict")
def predict(x: Car):
    pred = model.predict(x.dict())
    return int(pred)
