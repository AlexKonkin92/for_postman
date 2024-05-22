import logging 
import os
import threading

def bootstrap_ipa_api():
    from ipalib import create_api
    IPA_API = create_api(mode=None)
    logging.warning(f'in func: {IPA_API._API__done}')
    logging.warning(os.getpid())
    logging.warning(threading.current_thread())
    if 'finalize' in IPA_API._API__done:
        return IPA_API
    IPA_API.bootstrap()
    IPA_API.finalize()
    IPA_API.Backend.rpcclient.connect()
    return IPA_API
