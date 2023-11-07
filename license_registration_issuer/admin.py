from django.contrib import admin

from license_registration_issuer.models import Request


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    pass
