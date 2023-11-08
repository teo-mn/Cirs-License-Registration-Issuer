#!/bin/bash

echo 'Starting celery'
celery -A license_registration_issuer worker --beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --pool=solo --concurrency=1