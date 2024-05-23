FROM python
RUN apt-get update && apt-get install -y gcc libkrb5-dev libldap2-dev libsasl2-dev krb5-user ldap-utils python3-ipaclient

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt