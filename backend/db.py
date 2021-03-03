import sqlalchemy as sa
from pg_az_cert import secure_connect_ac 

import settings
from decorators import cache_to_file

def getconn():
    return secure_connect_ac(settings.APP_CONFIG_CONNECTION_STRING)

@cache_to_file("cache/schema.pckl")
def get_reflected_meta():
    meta = sa.MetaData(schema="prod")
    meta.reflect(bind=Engine)
    return meta

Engine = sa.create_engine("postgresql+psycopg2://",creator=getconn)
Meta = get_reflected_meta()
