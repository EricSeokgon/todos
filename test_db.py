import datetime
from database.db_connection import engine

try:
    with engine.connect() as conn:
        with open("db_res.txt", "w") as f:
            f.write(f"SUCCESS: Connection successful! @ {datetime.datetime.now()}\n")
except Exception as e:
    with open("db_res.txt", "w") as f:
        f.write(f"FAILED: {e} @ {datetime.datetime.now()}\n")
