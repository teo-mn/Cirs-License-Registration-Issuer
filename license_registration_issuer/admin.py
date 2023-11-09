from django.contrib import admin

from license_registration_issuer.models import Request, LatestSyncedBlock, EventLog


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    pass


@admin.register(LatestSyncedBlock)
class LatestSyncedBlockAdmin(admin.ModelAdmin):
    pass


@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    pass
