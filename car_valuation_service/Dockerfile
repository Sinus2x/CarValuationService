FROM python:3.10.2

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /requirements.txt

COPY app/ ./app/
COPY ml/ ./ml/

RUN mkdir /service
ENV PYTHONPATH=/service
WORKDIR /service

EXPOSE 8000

ENTRYPOINT ["uvicorn"]
CMD ["service:app", "--host", "0.0.0.0"]