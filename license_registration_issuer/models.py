import uuid
from django.db import models


class RequestType(models.TextChoices):
    REGISTER = 'REGISTER'
    REVOKE = 'REVOKE'
    UPDATE_DURATION = 'UPDATE_DURATION'
    ADD_EMPLOYEE = 'ADD_EMPLOYEE'
    REMOVE_EMPLOYEE = 'REMOVE_EMPLOYEE'
    ADD_REQUIREMENT = 'ADD_REQUIREMENT'
    REMOVE_REQUIREMENT = 'REMOVE_REQUIREMENT'


class RequestState(models.IntegerChoices):
    DRAFT = 0


class Request(models.Model):
    id = models.CharField(max_length=128, primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    request_type = models.CharField(
        choices=RequestType.choices,
        default=RequestType.REGISTER,
        max_length=20)
    state = models.IntegerField(
        choices=RequestState.choices,
        default=RequestState.DRAFT
    )
    callback_url = models.CharField(max_length=256, blank=True)
    data = models.CharField(max_length=2048, default='')
