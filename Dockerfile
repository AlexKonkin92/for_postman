FROM python:3.11
RUN apt-get update && apt-get install -y gcc libkrb5-dev libldap2-dev libsasl2-dev krb5-user ldap-utils freeipa-client python3-ipalib && apt-get clean && rm -rf /var/lib/apt/lists/*

#RUN apt-get update && apt-get install -y freeipa-client

WORKDIR /usr/src/app

#COPY ca.crt /etc/ipa/ca.crt
COPY try_for_freeipa.py ./
#COPY krb5.keytab /etc/krb5.keytab
#COPY krb5.conf /etc/krb5.conf

#ENV KRB5_CLIENT_KTNAME=/etc/krb5.keytab
#ENV KRB5CCNAME=FILE:/tmp/krb5cc_0

#RUN pip install ipalib ipaclient

COPY requirements.txt ./

RUN pip install -r requirements.txt
#CMD kinit admin@KS.WORKS -k -t /etc/krb5.keytab && python ./try_for_freeipa.py
CMD kinit host/freeipa-dev.ks.works@KS.WORKS -k -t /etc/krb5.keytab && python ./try_for_freeipa.py
#CMD ["python", "./try_for_freeipa.py"]