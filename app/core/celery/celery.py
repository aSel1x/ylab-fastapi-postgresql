from celery import Celery

from ..config import settings

# from .tasks import refresh_db_from_excel
from .tasks import refresh_db_from_google

celery = Celery('celery', broker=settings.rabbit_dns)

celery.conf.timezone = 'UTC'


# @celery.task
# def sync_db_with_excel():
#     refresh_db_from_excel()


@celery.task
def sync_db_with_google():
    refresh_db_from_google()


@celery.on_after_configure.connect
def setup_excel_task(sender, **kwargs):
    sender.add_periodic_task(15.0, sync_db_with_google.s())
    # sender.add_periodic_task(15.0, sync_db_with_excel.s())
