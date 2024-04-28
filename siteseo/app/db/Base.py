from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from dotenv import load_dotenv
import os
load_dotenv()
SCHEMA = os.getenv("db_schema")
metadata = MetaData(schema=SCHEMA)
Base = declarative_base(metadata=metadata)