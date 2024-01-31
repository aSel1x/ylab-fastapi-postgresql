import os

db_usr = os.environ["DB_USER"]
db_pwd = os.environ["DB_PASSWORD"]
db_host = os.environ["DB_HOST"]
db_prt = os.environ["DB_PORT"]
db_name = os.environ["DB_NAME"]

if os.environ["TEST_MODE"] == '0':
    BASE_URL = "/api/v1"
else:
    BASE_URL = "/test-api/v1"


# Raspberry pi local server with hosted on PostgresSQL YLAB database
DB_URL = f"postgresql://{db_usr}:{db_pwd}@{db_host}:{db_prt}/{db_name}"
DB_ORM_URL = f"postgresql+asyncpg://{db_usr}:{db_pwd}@{db_host}:{db_prt}/{db_name}"
