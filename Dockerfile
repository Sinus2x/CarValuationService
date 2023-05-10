FROM python:3.10

WORKDIR workdir
COPY requirements.txt /workdir/
RUN pip install -r requirements.txt

COPY app/ ./app/
COPY ml/ ./ml/
COPY models/model_no_text ./models/


CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8080"]