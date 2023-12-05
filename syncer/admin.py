from django.contrib import admin

from syncer.models import LatestSyncedBlock, EventLog


@admin.register(LatestSyncedBlock)
class LatestSyncedBlockAdmin(admin.ModelAdmin):
    pass


@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    pass
