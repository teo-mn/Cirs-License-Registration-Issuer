from django.db import models


class LatestSyncedBlock(models.Model):
    last_synced_block_kv = models.IntegerField(default=-1)
    last_synced_block_license = models.IntegerField(default=-1)
    last_synced_block_requirement = models.IntegerField(default=-1)


class EventType(models.TextChoices):
    SET_DATA = 'SET_DATA'
    LICENSE_REGISTERED = 'LICENSE_REGISTERED'
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


class EventLog(models.Model):
    id = models.CharField(max_length=128, primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    tx = models.CharField(max_length=128)
    log_type = models.CharField(
        choices=EventType.choices,
        max_length=32)
    block_number = models.IntegerField()
    contract_address = models.CharField(max_length=128)
    timestamp = models.IntegerField()
    license_id = models.CharField(max_length=1024, default='', blank=True)
    license_name = models.CharField(max_length=1024, default='', blank=True)
    owner_id = models.CharField(max_length=1024, default='', blank=True)
    owner_name = models.CharField(max_length=1024, default='', blank=True)
    start_date = models.IntegerField(default=0)
    end_date = models.IntegerField(default=0)
    additional_data = models.CharField(max_length=1024, default='', blank=True)
    requirement_id = models.CharField(max_length=1024, default='', blank=True)
    evidence_id = models.CharField(max_length=1024, default='', blank=True)
    requirement_name = models.CharField(max_length=1024, default='', blank=True)
    key = models.CharField(max_length=1024, default='', blank=True)
    value = models.CharField(max_length=1024, default='', blank=True)


class LicenseProduct(models.Model):
    id = models.CharField(max_length=128, primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    name = models.CharField(max_length=255)
    license_address = models.CharField(max_length=128, unique=True)
    requirement_address = models.CharField(max_length=128)
    kv_address = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)


class License(models.Model):
    id = models.CharField(max_length=128, primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    license_id = models.CharField(max_length=1024, default='', blank=True)
    license_name = models.CharField(max_length=1024, default='', blank=True)
    owner_id = models.CharField(max_length=1024, default='', blank=True)
    owner_name = models.CharField(max_length=1024, default='', blank=True)
    start_date = models.IntegerField(default=0)
    end_date = models.IntegerField(default=0)
    state = models.CharField(max_length=128)
    tx = models.CharField(max_length=128)
    license_address = models.CharField(max_length=128, default='')


class LicenseRequirements(models.Model):
    id = models.CharField(max_length=128, primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    license_id = models.CharField(max_length=1024, default='', blank=True)
    requirement_id = models.CharField(max_length=1024, default='', blank=True)
    requirement_name = models.CharField(max_length=1024, default='', blank=True)
    state = models.CharField(max_length=128)
    tx = models.CharField(max_length=128)
    license_address = models.CharField(max_length=128, default='')


class Evidence(models.Model):
    id = models.CharField(max_length=128, primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    license_id = models.CharField(max_length=1024, default='', blank=True)
    requirement_id = models.CharField(max_length=1024, default='', blank=True)
    evidence_id = models.CharField(max_length=1024, default='', blank=True)
    key = models.CharField(max_length=1024, default='', blank=True)
    value = models.CharField(max_length=1024, default='', blank=True)
