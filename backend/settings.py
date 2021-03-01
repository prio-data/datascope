"""
Settings and globals
"""
import os
from environs import Env

env = Env()
env.read_env()

# =GLOBALS===========================================================

BASE_PATH = os.path.split(os.path.abspath(__file__))[0]
CERT_FOLDER=env.str("CERT_FOLDER","certs")
DEVSERVER = "http://localhost:8080/"

# =SETTINGS==========================================================

HOST=env.str('HOST')
PORT=env.str('PORT')
DBNAME=env.str('DBNAME')
SCHEMA=env.str("SCHEMA")

KEY_VAULT_URL=env.str("KEY_VAULT_URL")

_certnames = [env.str(k) for k in ("SSL_CERT","SSL_KEY","SSL_ROOT_CERT")]
_certpaths = (os.path.join(BASE_PATH,CERT_FOLDER,v) for v in _certnames)
CERT_PATH,KEY_PATH,ROOT_CERT_PATH = _certpaths

PRODUCTION = env.bool("PRODUCTION",False)
