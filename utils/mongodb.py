import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

#DB = os.getenv("MONGO_DB_NAME") or os.getenv("MONGO_DB_NAME")
DB = os.getenv("MONGO_DB_NAME") or os.getenv("MONGO_DB_NAME")
URI = os.getenv("MONGODB_URI") or os.getenv("URI")

if not DB:
    raise ValueError("Database name not found. set DATABASE_NAME or MONGO_DB_NAME environmet variable")
if not URI:
    raise ValueError("MongoDB URI not found. set MONGODB_URI or URI enviroment variable")


_client = None
def get_mongo_client():
    global _client
    if _client is None:
        _client = MongoClient(
            URI,
            server_api=ServerApi("1"),
            tls=True,
            tlsAllowInvalidCertificates= True,
            serverSelectionTimeoutMS =5000
        )
    return _client


def get_collection(col):
    client = get_mongo_client()
    return client[DB][col]

def t_connection():
    try:
        client = get_mongo_client()
        client.admin.command("ping")
        return True
    except Exception as e:
        print(f"Error conectando a MongoDB ")
        return False
    
    
    
"""def get_collection( col ):
    client = MongoClient(  
        URI
        , server_api = ServerApi("1")
        , tls = True
        , tlsAllowInvalidCertificates = True
    )
    client.admin.command("ping")
    return client[DB][col]"""




###########VIDEO ---11     MINUTOOOOOO 29    ACTUALIZARRR TOD