from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from ..config import settings

engine = create_engine(settings.sync_pg_dns)


def get_db() -> Session:
    with Session(bind=engine, expire_on_commit=False) as session:
        return session
