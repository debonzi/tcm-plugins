from functools import wraps

def backend_handler(f):
    @wraps(f)
    def handler(*args, **kargs):
        c_obj, = args
        c_backend_name = kargs['backend']
        if f.__module__.split('.')[-1] == c_backend_name:
            f(*args, **kargs)
    return handler
