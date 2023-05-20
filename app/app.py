from fastapi import FastAPI
from ml.datatypes import Car
from ml.model import Model
from gensim.models.word2vec import Word2Vec
from gensim.models import KeyedVectors
from pathlib import Path
import pandas as pd
import pickle

model = None
features_models_dict = None
app = FastAPI()


# create a route
@app.get("/")
def index():
    return {"text": "Welcome to Car Valuation Service!"}


# Register the function to run during startup
@app.on_event("startup")
def startup_event():
    global model
    global features_models_dict
    # equipment modes
    modes_path = "data/weights/equipment_modes.csv"
    path = Path(__file__).parent.parent / modes_path
    equipment_modes = pd.read_csv(path)

    # base_price_grouper
    weights_save_path = "data/weights/base_price_grouper.csv"
    path = Path(__file__).parent.parent / weights_save_path
    base_price_grouper = pd.read_csv(path)

    # desc w2v
    model_save_path = Path(__file__).parent.parent / 'data/weights/desc_w2v_model'
    word_vectors_save_path = Path(__file__).parent.parent / 'data/weights/desc_w2v_word_vectors'
    w2v_model = Word2Vec.load(str(model_save_path))
    w2v_model_wv = KeyedVectors.load(str(word_vectors_save_path), mmap='r')

    # desc tf-idf
    model_save_path = Path(__file__).parent.parent / 'data/weights/desc_tfidf_model.pkl'
    with open(model_save_path, 'rb') as f:
        tfidf = pickle.load(f)

    # eq w2v
    model_save_path = Path(__file__).parent.parent / 'data/weights/equip_w2v_model'
    word_vectors_save_path = Path(__file__).parent.parent / 'data/weights/equip_w2v_word_vectors'
    equipment_w2v_model = Word2Vec.load(str(model_save_path))
    equipment_w2v_model_wv = KeyedVectors.load(str(word_vectors_save_path), mmap='r')

    # mod w2v
    model_save_path = Path(__file__).parent.parent / 'data/weights/modification_w2v_model'
    word_vectors_save_path = Path(__file__).parent.parent / 'data/weights/modification_w2v_word_vectors'
    modification_w2v_model = Word2Vec.load(str(model_save_path))
    modification_w2v_model_wv = KeyedVectors.load(str(word_vectors_save_path), mmap='r')

    features_models_dict = {
        "base_price_grouper": base_price_grouper,
        "equipment_modes": equipment_modes,
        "w2v_model": w2v_model,
        "w2v_model_wv": w2v_model_wv,
        "tfidf": tfidf,
        "eq_w2v_model": equipment_w2v_model,
        "eq_w2v_model_wv": equipment_w2v_model_wv,
        "mod_w2v_model": modification_w2v_model,
        "mod_w2v_model_wv": modification_w2v_model_wv,
    }

    model = Model(models_dict=features_models_dict)


@app.post("/predict")
def predict(x: Car):
    pred = model.predict(x.dict())
    return int(pred)
