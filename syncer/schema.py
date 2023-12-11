import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType

from syncer.models import LicenseProduct, License, Evidence, LicenseRequirements, EventLog


class LicenseProductNode(DjangoObjectType):
    class Meta:
        model = LicenseProduct
        fields = ("id", "name", "license_address", "requirement_address", "kv_address")


class EvidenceNode(DjangoObjectType):
    class Meta:
        model = Evidence
        fields = ("id", "evidence_id", "tx", "timestamp", "state", "license_id", "requirement_id",
                  "product", "additional_data")


class RequirementNode(DjangoObjectType):
    evidences = graphene.List(EvidenceNode)

    class Meta:
        model = LicenseRequirements
        fields = ("id", "tx", "timestamp", "requirement_id", "requirement_name", "state", "evidences",
                  "license_id", "product", "additional_data")

    def resolve_evidences(self, info):
        return Evidence.objects.filter(requirement_id=self.requirement_id,
                                       license_id=self.license_id,
                                       product__id=self.product.id).all()


class LicenseNode(DjangoObjectType):
    requirements = graphene.List(RequirementNode)

    class Meta:
        model = License
        fields = ("id", "tx", "state", "license_id", "license_name", "owner_id", "owner_name",
                  "start_date", "end_date", "additional_data", "timestamp", "product", "additional_data")

    def resolve_requirements(self, info):
        return LicenseRequirements.objects.filter(license_id=self.license_id, product__id=self.product.id).all()


class LogNode(DjangoObjectType):
    class Meta:
        model = EventLog
        fields = ("id", "tx", "timestamp", "license_id", "license_name", "owner_id", "owner_name",
                  "start_date", "end_date", "additional_data", "timestamp", "log_type",
                  "requirement_id", "requirement_name", "evidence_id", "key", "value")


class QueryProducts(graphene.ObjectType):
    products = graphene.List(LicenseProductNode, search=graphene.String(required=False))
    product = graphene.Field(LicenseProductNode, license_address=graphene.String())

    def resolve_products(root, info, search=''):
        if search is not None and search != '':
            query = LicenseProduct.objects.filter(
                Q(name__icontains=search) | Q(license_address__iexact=search)
                | Q(requirement_address__iexact=search)
                | Q(kv_address__iexact=search)
            )
        else:
            query = LicenseProduct.objects
        return query.filter(is_active=True).order_by('created_at').all()

    def resolve_product(self, info, license_address):
        try:
            return LicenseProduct.objects.get(license_address=license_address, is_active=True)
        except LicenseProduct.DoesNotExist:
            return None


class QueryLicenses(graphene.ObjectType):
    licenses = graphene.List(LicenseNode, license_address=graphene.String(), search=graphene.String(required=False))
    license = graphene.Field(LicenseNode, license_address=graphene.String(), license_id=graphene.String())

    def resolve_licenses(self, info, license_address, search=''):
        # We can easily optimize query count in the resolve method
        if search is not None and search != '':
            query = License.objects.filter(
                Q(license_id__icontains=search) |
                Q(license_name__icontains=search) |
                Q(owner_id__icontains=search) |
                Q(owner_name__icontains=search) |
                Q(tx__iexact=search)
            )
        else:
            query = License.objects
        return query.filter(product__license_address=license_address).order_by('-created_at').all()

    def resolve_license(self, info, license_address, license_id):
        try:
            return License.objects.get(product__license_address=license_address, license_id=license_id)
        except License.DoesNotExist:
            return None


class QueryRequirements(graphene.ObjectType):
    requirements = graphene.List(RequirementNode, license_address=graphene.String(), license_id=graphene.String())

    def resolve_requirements(self, info, license_address, license_id):
        return LicenseRequirements.objects.filter(product__license_address=license_address,
                                                  license_id=license_id).all()


class EvidenceDetailNode(graphene.ObjectType):
    evidences = graphene.List(EvidenceNode)
    # requirements = graphene.List(RequirementNode, license_id=graphene.String(required=True))
    logs = graphene.List(LogNode)

    def resolve_evidences(self, info):
        if self['evidence_id'] is None or self['evidence_id'] == '':
            return []
        return Evidence.objects.filter(product__license_address=self['license_address'],
                                       evidence_id=self['evidence_id'])

    def resolve_logs(self, info):
        if self['evidence_id'] is None or self['evidence_id'] == '':
            return []
        return EventLog.objects.filter(product__license_address=self['license_address'],
                                       evidence_id=self['evidence_id']).all()


class QueryEvidences(graphene.ObjectType):
    evidence = graphene.Field(EvidenceDetailNode, license_address=graphene.String(required=True),
                              evidence_id=graphene.String(required=True))

    def resolve_evidence(self, info, license_address, evidence_id):
        return {'license_address': license_address, 'evidence_id': evidence_id}


class Query(QueryProducts, QueryLicenses, QueryRequirements, QueryEvidences):
    logs = graphene.List(LogNode, license_address=graphene.String(required=True),
                         license_id=graphene.String(required=True))

    def resolve_logs(self, info, license_address, license_id):
        return EventLog.objects.filter(product__license_address=license_address) \
            .filter(license_id=license_id).order_by('-timestamp').all()


schema = graphene.Schema(query=Query)
