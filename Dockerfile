FROM python:3.9
RUN apt-get update && apt-get install -y gcc libkrb5-dev libldap2-dev libsasl2-dev krb5-user ldap-utils freeipa-client python3-ipalib && apt-get clean && rm -rf /var/lib/apt/lists/*

#RUN apt-get update && apt-get install -y freeipa-client

WORKDIR /usr/src/app

COPY ca.crt /etc/ipa/ca.crt
COPY try_for_freeipa.py ./

RUN pip install ipalib ipaclient

#COPY requirements.txt ./

#RUN pip install -r requirements.txt
CMD ["python", "./try_for_freeipa.py"]