FROM python:3.11
#RUN apt-get update && apt-get install -y gcc libkrb5-dev libldap2-dev libsasl2-dev krb5-user ldap-utils freeipa-client python3-ipalib && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY rpc_flask.py ./
COPY requirements.txt ./

RUN pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "rpc_flask:app"]