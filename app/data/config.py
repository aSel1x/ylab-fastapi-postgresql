import os

db_usr = os.environ["DB_USER"]
db_pwd = os.environ["DB_PASSWORD"]


# Raspberry pi local server with hosted on PostgresSQL YLAB database
DB_URL = f"postgresql://{db_usr}:{db_pwd}@192.168.0.104:5432/ylab"
BASE_URL = "/api/v1"
