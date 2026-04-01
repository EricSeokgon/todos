import datetime
from database.db_connection import engine
import models

try:
    with engine.connect() as conn:
        with open("db_res.txt", "w") as f:
            f.write(f"SUCCESS: Connection successful! @ {datetime.datetime.now()}\n")
    
    models.Base.metadata.create_all(bind=engine)
    with open("db_res.txt", "a") as f:
        f.write("SUCCESS: Table creation executed!\n")
except Exception as e:
    with open("db_res.txt", "w") as f:
        f.write(f"FAILED: {e} @ {datetime.datetime.now()}\n")
