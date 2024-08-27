from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import settings

SQLALCHEMY_DATABASE_URL = "postgresql://"+settings.PG_USER+":"+settings.PG_PASSWD+"@"+settings.PG_HOST+":"+settings.PG_PORT+"/"+settings.PG_DBNAME

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,echo=True,  pool_size=10, max_overflow=20
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()