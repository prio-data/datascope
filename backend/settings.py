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
CACHE_DIR = "cache"

try:
    os.makedirs(CACHE_DIR)
except FileExistsError:
    pass

try:
    os.makedirs(CERT_FOLDER)
except FileExistsError:
    pass

# =SETTINGS==========================================================

APP_CONFIG_CONNECTION_STRING=env.str("APP_CONFIG_CONNECTION_STRING")

CERT_FOLDER=env.str("CERT_FOLDER")

PRODUCTION = env.bool("PRODUCTION",False)
