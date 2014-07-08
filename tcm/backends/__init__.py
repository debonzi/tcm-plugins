import imp
from tcm.backends import (
    smt,
    telmex
)

def get_pbe_info(backend_name):
    try:
        f, fn, d = imp.find_module('model', ['tcm/backends/%s'%backend_name])
        be = imp.load_module(backend_name, f, fn, d)
        if hasattr(be, 'get_model_repr'):
            return be.get_model_repr
    except ImportError:
        return





