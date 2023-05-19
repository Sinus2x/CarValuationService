FROM python:3.10.2

WORKDIR workdir
COPY requirements.txt /workdir/
RUN pip install -r requirements.txt

COPY app/ ./app/
COPY ml/ ./ml/

COPY data/weights/model ./data/weights/

COPY data/weights/base_price_grouper_weights.pkl ./data/weights/
COPY data/weights/desc_tfidf_model.pkl ./data/weights/
COPY data/weights/desc_w2v_model ./data/weights/
COPY data/weights/desc_w2v_word_vectors ./data/weights/
COPY data/weights/equip_w2v_model ./data/weights/
COPY data/weights/equip_w2v_word_vectors ./data/weights/
COPY data/weights/equipment_modes.csv ./data/weights/
COPY data/weights/modification_w2v_model ./data/weights/
COPY data/weights/modification_w2v_word_vectors ./data/weights/



CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8080"]