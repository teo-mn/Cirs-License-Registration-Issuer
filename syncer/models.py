import uuid

from django.db import models


class LatestSyncedBlock(models.Model):
    last_synced_block_number = models.IntegerField(default=0)


class BlockchainState(models.TextChoices):
    REGISTERED = 'REGISTERED'
    REVOKED = 'REVOKED'


class EventType(models.TextChoices):
    SET_DATA = 'SET_DATA'
    LICENSE_REGISTERED = 'LICENSE_REGISTERED'
    LICENSE_UPDATED = 'LICENSE_UPDATED'
    LICENSE_REVOKED = 'LICENSE_REVOKED'
    REQUIREMENT_REGISTERED = 'REQUIREMENT_REGISTERED'
    REQUIREMENT_REVOKED = 'REQUIREMENT_REVOKED'
    EVIDENCE_REGISTERED = 'EVIDENCE_REGISTERED'
    EVIDENCE_REVOKED = 'EVIDENCE_REVOKED'

    @classmethod
    def from_name(cls, event_name):
        if event_name == 'SetData':
            return EventType.SET_DATA
        elif event_name == 'LicenseRegistered':
            return EventType.LICENSE_REGISTERED
        elif event_name == 'LicenseRevoked':
            return EventType.LICENSE_REVOKED
        elif event_name == 'LicenseRequirementRegistered':
            return EventType.REQUIREMENT_REGISTERED
        elif event_name == 'LicenseRequirementRevoked':
            return EventType.REQUIREMENT_REVOKED
        elif event_name == 'EvidenceRegistered':
            return EventType.EVIDENCE_REGISTERED
        elif event_name == 'EvidenceRevoked':
            return EventType.EVIDENCE_REVOKED


class LicenseProduct(models.Model):
    id = models.CharField(max_length=128, primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    name = models.CharField(max_length=255)
    license_address = models.CharField(max_length=128, unique=True)
    requirement_address = models.CharField(max_length=128)
    kv_address = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)


class KV(models.Model):
    id = models.CharField(max_length=128, primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey(LicenseProduct, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    key = models.CharField(max_length=1024, default='', blank=True)
    value = models.CharField(max_length=1024, default='', blank=True)
    timestamp = models.BigIntegerField(default=0)
    tx = models.CharField(max_length=128, default='')


class EventLog(models.Model):
    id = models.CharField(max_length=128, primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey(LicenseProduct, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    tx = models.CharField(max_length=128)
    log_type = models.CharField(
        choices=EventType.choices,
        max_length=32)
    block_number = models.IntegerField()
    timestamp = models.BigIntegerField()
    license_id = models.CharField(max_length=1024, default='', blank=True)
    license_name = models.CharField(max_length=1024, default='', blank=True)
    owner_id = models.CharField(max_length=1024, default='', blank=True)
    owner_name = models.CharField(max_length=1024, default='', blank=True)
    start_date = models.BigIntegerField(default=0)
    end_date = models.BigIntegerField(default=0)
    additional_data = models.CharField(max_length=1024, default='', blank=True)
    additional_data_kv = models.ForeignKey(KV, on_delete=models.CASCADE, null=True)
    requirement_id = models.CharField(max_length=1024, default='', blank=True)
    evidence_id = models.CharField(max_length=1024, default='', blank=True)
    requirement_name = models.CharField(max_length=1024, default='', blank=True)
    key = models.CharField(max_length=1024, default='', blank=True)
    value = models.CharField(max_length=1024, default='', blank=True)


class License(models.Model):
    id = models.CharField(max_length=128, primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey(LicenseProduct, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    license_id = models.CharField(max_length=1024, default='', blank=True)
    license_name = models.CharField(max_length=1024, default='', blank=True)
    owner_id = models.CharField(max_length=1024, default='', blank=True)
    owner_name = models.CharField(max_length=1024, default='', blank=True)
    additional_data = models.CharField(max_length=1024, default='', blank=True)
    additional_data_kv = models.ForeignKey(KV, on_delete=models.CASCADE, null=True)
    additional_data_json = models.JSONField(default=dict)
    start_date = models.BigIntegerField(default=0)
    end_date = models.BigIntegerField(default=0)
    state = models.CharField(
        choices=BlockchainState.choices,
        max_length=32)
    tx = models.CharField(max_length=128)
    timestamp = models.BigIntegerField(default=0)


class LicenseRequirements(models.Model):
    id = models.CharField(max_length=128, primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey(LicenseProduct, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    license_id = models.CharField(max_length=1024, default='', blank=True)
    requirement_id = models.CharField(max_length=1024, default='', blank=True)
    requirement_name = models.CharField(max_length=1024, default='', blank=True)
    additional_data = models.CharField(max_length=1024, default='', blank=True)
    additional_data_kv = models.ForeignKey(KV, on_delete=models.CASCADE, null=True)
    state = models.CharField(
        choices=BlockchainState.choices,
        max_length=32)
    tx = models.CharField(max_length=128)
    timestamp = models.BigIntegerField(default=0)
    license_obj = models.ForeignKey(License, on_delete=models.CASCADE, null=True)


class Evidence(models.Model):
    id = models.CharField(max_length=128, primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey(LicenseProduct, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    license_id = models.CharField(max_length=1024, default='', blank=True)
    requirement_id = models.CharField(max_length=1024, default='', blank=True)
    evidence_id = models.CharField(max_length=1024, default='', blank=True)
    key = models.CharField(max_length=1024, default='', blank=True)
    value = models.CharField(max_length=1024, default='', blank=True)
    additional_data = models.CharField(max_length=1024, default='', blank=True)
    additional_data_kv = models.ForeignKey(KV, on_delete=models.CASCADE, null=True)
    evidence_kv = models.ForeignKey(KV, on_delete=models.CASCADE, null=True, related_name='evidence_kv')
    timestamp = models.BigIntegerField(default=0)
    tx = models.CharField(max_length=128, default='')
    state = models.CharField(
        choices=BlockchainState.choices,
        max_length=32)
    requirement_obj = models.ForeignKey(LicenseRequirements, on_delete=models.CASCADE, null=True)
