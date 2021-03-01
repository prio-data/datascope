import os
import json
import pickle
from functools import wraps

FILE_HANDLERS = {
        ".json":(json.dump,json.load,False),
        ".pckl":(pickle.dump,pickle.load,True),
    }

def cache_to_file(filename):
    dump,load,is_bytes = FILE_HANDLERS[os.path.splitext(filename)[-1]]
    def dec(fn):
        @wraps(fn)
        def inner(*args,**kwargs):
            if not os.path.exists(filename):
                res = fn(*args,**kwargs)
                with open(filename,"w"+("b" if is_bytes else "")) as f:
                    dump(res,f)
            else:
                with open(filename,"r"+("b" if is_bytes else "")) as f:
                    res = load(f)
            return res
        return inner
    return dec
