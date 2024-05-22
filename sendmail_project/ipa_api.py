import logging 

def bootstrap_ipa_api():
    logging.warning(f'in func before: {IPA_API._API__done}')
    from ipalib import api as IPA_API
    logging.warning(f'in func: {IPA_API._API__done}')
    #IPA_API.bootstrap()
    #IPA_API.finalize()
    IPA_API.Backend.rpcclient.connect()
    return IPA_API
