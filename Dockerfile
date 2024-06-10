FROM python:3.11

WORKDIR /usr/src/app

COPY rpc_flask.py ./
COPY requirements.txt ./
COPY config.py ./
COPY .env ./

RUN pip install python-dotenv

RUN pip install -r requirements.txt

ENV ENV_FILE .env

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "rpc_flask:app"]