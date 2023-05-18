FROM python:3.10

WORKDIR workdir
COPY requirements.txt /workdir/
RUN pip install -r requirements.txt

COPY app/ ./app/
COPY ml/ ./ml/
COPY data/weights/model_no_text ./data/weights/


CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8080"]