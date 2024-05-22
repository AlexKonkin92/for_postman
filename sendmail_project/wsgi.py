"""
WSGI config for sendmail_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from ipalib import api
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sendmail_project.settings')

if not api.isdone('bootstrap'):
    api.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works')
    api.finalize()
    api.Backend.rpcclient.connect()

application = get_wsgi_application()
