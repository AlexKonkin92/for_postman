FROM python:3.11

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

ENV ENV_FILE .env

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "rpc_flask:app"]