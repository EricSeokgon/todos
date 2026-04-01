from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import urllib.parse

password = urllib.parse.quote_plus("")
DATABASE_URL = f"mysql+pymysql://root:{password}@:3306/fastapi_db"

engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
