import os
import pickle
import sqlalchemy as sa
from psycopg2 import connect

from azure.identity import (
        ManagedIdentityCredential,
        EnvironmentCredential,
        AzureCliCredential
    )
from azure.identity._exceptions import CredentialUnavailableError
from azure.keyvault.secrets import SecretClient 
from azure.core.exceptions import (
        ResourceNotFoundError,
        ServiceRequestError,
        HttpResponseError
    )

from exceptions import ConfigError
import settings
from decorators import cache_to_file

"""
Fetch certs from Azure Key Vault
"""

if settings.PRODUCTION:
    AZ_CREDS = ManagedIdentityCredential()
    try:
        AZ_CREDS.get_token()
    except CredentialUnavailableError:
        AZ_CREDS = EnvironmentCredential()
else:
    AZ_CREDS = AzureCliCredential()

KV_CLIENT = SecretClient(vault_url=settings.KEY_VAULT_URL, credential=AZ_CREDS)
certnames = [env.str(name) for name in ("DB_SSL_CERT","DB_SSL_KEY","DB_SSL_ROOTCERT")]
cert_filenames = [os.path.join(settings.CERT_FOLDER,name) for name in certnames]

try:
    os.makedirs(settings.CERT_FOLDER)
except FileExistsError:
    pass

if not all([os.path.exists(filename) for filename in cert_filenames]):
    for cert_name,filename in zip(certnames,cert_filenames): 
        try:
            cert_str = KV_CLIENT.get_secret(cert_name)
        except ResourceNotFoundError as e:
            raise ConfigError("You have not defined the secret yet") from e
        except ServiceRequestError as e:
            raise ConfigError("Didn't find vault (bad credentials?)") from e
        except HttpResponseError as e:
            raise ConfigError("You don't have permission to GET this secret.") from e

        with open(filename,"w") as f:
            f.write(cert_str.value)
        os.chmod(filename,0o600)


connection_string = f"""
        host={settings.HOST}
        port={settings.PORT}
        dbname={settings.DBNAME}
        sslcert={settings.CERT_PATH}
        sslkey={settings.KEY_PATH}
        sslrootcert={settings.ROOT_CERT_PATH}
        sslmode=require
"""

def getconn():
    return connect(connection_string)

@cache_to_file("cache/schema.pckl")
def get_reflected_meta():
    meta = sa.MetaData(schema="prod")
    meta.reflect(bind=Engine)
    print(meta.tables)
    return meta

Engine = sa.create_engine("postgresql+psycopg2://",creator=getconn)
Meta = get_reflected_meta()
