import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

from license_registration_issuer.settings import SYNCER_CRON_JOB_MINUTE, SYNCER_ON

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'license_registration_issuer.settings')

app = Celery('license_registration_issuer')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.on_after_configure.connect
def schedule_periodic_tasks(sender, **kwargs):
    # blockchain event syncer
    if SYNCER_ON:
        sender.add_periodic_task(crontab(minute=SYNCER_CRON_JOB_MINUTE), task_sync.s(text='Task'))


@app.task(bind=True)
def task_sync(self, text):
    from syncer.syncer import BlockSyncer
    syncer = BlockSyncer()
    syncer.syn_new_blocks()
