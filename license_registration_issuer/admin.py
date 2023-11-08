from django.contrib import admin

from license_registration_issuer.models import Request, LatestSyncedBlock


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    pass


@admin.register(LatestSyncedBlock)
class LatestSyncedBlockAdmin(admin.ModelAdmin):
    pass
