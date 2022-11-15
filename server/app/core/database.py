# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE_HOST, DATABASE_PORT, DATABASE_USER, DATABASE_PASSWORD, DATABASE_DB
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

SQLALCHEMY_DATABASE_URL = "sqlite:///./bx_saas.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# SQLALCHEMY_DATABASE_URL = "mysql+pymysq://" + DATABASE_USER + ":" + DATABASE_PASSWORD + "@" + \
#                           DATABASE_HOST + ":" + DATABASE_PORT + "/" + DATABASE_DB
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
# )

DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()




