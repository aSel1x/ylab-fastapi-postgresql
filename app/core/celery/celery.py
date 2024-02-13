from celery import Celery

from ..config import settings
from .tasks import refresh_db_from_excel

# from .tasks import refresh_db_from_google

celery = Celery('celery', broker=settings.rabbit_dns)
celery.conf.timezone = 'UTC'


def once(func):
    def wrapper(*args, **kwargs):
        lock_key = f'celery_lock_{func.__name__}'
        if settings.redis.get(lock_key):
            print('Task is already running, skipping execution.')
            return

        settings.redis.set(lock_key, 'true', ex=60)
        try:
            return func(*args, **kwargs)
        finally:
            settings.redis.delete(lock_key)
    return wrapper


@celery.task(ignore_result=True)
@once
def sync_db_with_excel():
    refresh_db_from_excel()


# @celery.task(ignore_result=True)
# @once
# def sync_db_with_google():
#     refresh_db_from_google()


@celery.on_after_configure.connect
def setup_excel_task(sender, **kwargs):
    # sender.add_periodic_task(15.0, sync_db_with_google.s())
    sender.add_periodic_task(15.0, sync_db_with_excel.s())
