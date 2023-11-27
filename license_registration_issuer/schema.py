import graphene
from graphene_django import DjangoObjectType

from license_registration_issuer.models import LicenseProduct, EventLog, License, LicenseRequirements, Evidence


class LicenseProductType(DjangoObjectType):
    class Meta:
        model = LicenseProduct
        fields = ("id", "name", "license_address", "requirement_address", "kv_address")


class LicenseType(DjangoObjectType):
    class Meta:
        model = License
        fields = ("id", "tx", "state", "license_id", "license_name", "owner_id", "owner_name",
                  "start_date", "end_date", "additional_data")


class EvidenceNode(DjangoObjectType):
    class Meta:
        model = Evidence
        fields = ("id", "evidence_id")


class RequirementType(DjangoObjectType):
    evidences = graphene.List(EvidenceNode)

    class Meta:
        model = LicenseRequirements
        fields = ("id", "tx", "requirement_id", "requirement_name", "state", "evidences")

    def resolve_evidences(self, info):
        return Evidence.objects.all()


class LogType(DjangoObjectType):
    class Meta:
        model = EventLog
        fields = ("id", "tx", "license_id", "license_name", "owner_id", "owner_name",
                  "start_date", "end_date", "additional_data")


class Query(graphene.ObjectType):
    products = graphene.List(LicenseProductType)
    product = graphene.Field(LicenseProductType, license_address=graphene.String())

    licenses = graphene.List(LicenseType, license_address=graphene.String())
    license = graphene.Field(LicenseType, license_address=graphene.String(), license_id=graphene.String())
    requirements = graphene.List(RequirementType, license_address=graphene.String(), license_id=graphene.String())

    logs = graphene.List(LogType, license_address=graphene.String(), license_id=graphene.String())

    def resolve_products(root, info):
        # We can easily optimize query count in the resolve method
        return LicenseProduct.objects.filter(is_active=True).order_by('created_at').all()

    def resolve_product(self, info, license_address):
        try:
            return LicenseProduct.objects.get(license_address=license_address)
        except LicenseProduct.DoesNotExist:
            return None

    def resolve_licenses(root, info, license_address):
        # We can easily optimize query count in the resolve method
        return License.objects.filter(license_address=license_address).order_by('-created_at').all()

    def resolve_license(self, info, license_address, license_id):
        try:
            return License.objects.get(license_address=license_address, license_id=license_id)
        except License.DoesNotExist:
            return None

    def resolve_logs(self, info, license_address, license_id):
        return EventLog.objects.filter(contract_address=license_address,
                                       license_id=license_id).order_by('-timestamp').all()

    def resolve_requirements(self, info, license_address, license_id):
        return LicenseRequirements.objects.filter().all()


schema = graphene.Schema(query=Query)
