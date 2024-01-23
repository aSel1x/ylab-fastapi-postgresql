import os
import argparse

# db_usr = os.environ["DB_USER"]
# db_pwd = os.environ["DB_PASSWORD"]
parser = argparse.ArgumentParser()
parser.add_argument(
    '-db-url', '--db-url',
    dest='db_url',
    required=True
)
parser.add_argument(
    '-db-prt', '--db-port',
    dest='db_port',
    required=True
)
parser.add_argument(
    '-db-nm', '-db-name',
    dest='db_name',
    required=True
)
parser.add_argument(
    '-db-usr', '-db-user',
    dest='db_user',
    required=True
)
parser.add_argument(
    '-db-pwd', '-db-password',
    dest='db_password',
    required=True
)
args = parser.parse_args()
db_url = args.db_url
db_prt = args.db_port
db_name = args.db_name
db_usr = args.db_user
db_pwd = args.db_password


# Raspberry pi local server with hosted on PostgresSQL YLAB database
DB_URL = f"postgresql://{db_usr}:{db_pwd}@{db_url}:{db_prt}/{db_name}"
BASE_URL = "/api/v1"
