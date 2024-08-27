from dotenv import dotenv_values
from typing import List
dotenv_config = dotenv_values('config.env')
class Settings:
    BACKEND_CORS_ORIGINS: List = ['*']
    # APP
    APP_HOST = dotenv_config.get("APP_HOST", "127.0.0.1")
    APP_PORT = int(dotenv_config.get("APP_PORT", 8000))

    # pgsql
    PG_HOST = dotenv_config.get("PG_HOST", "")
    PG_PORT = dotenv_config.get("PG_PORT", "")
    PG_DBNAME = dotenv_config.get("PG_DBNAME", "")
    PG_USER = dotenv_config.get("PG_USER", "")
    PG_PASSWD = dotenv_config.get("PG_PASSWD", "")

    #swagger
    PROXY_PATH = dotenv_config.get("PROXY_PATH", "")
settings = Settings()
