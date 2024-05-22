import logging
import threading
from ipalib import api as IPA_API

initialization_lock = threading.Lock()

def bootstrap_ipa_api():
    with initialization_lock:
        logging.warning(f'in func: {IPA_API._API__done}')
        logging.warning(threading.current_thread())
        if 'finalize' in IPA_API._API__done:
            logging.warning('IPA API is already bootstrapped.')
            return IPA_API
        logging.warning('Bootstrapping IPA API.')
        IPA_API.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works')
        IPA_API.finalize()
        IPA_API.Backend.rpcclient.connect()
    return IPA_API
