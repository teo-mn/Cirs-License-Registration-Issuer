import time

import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType

from syncer.models import LicenseProduct, License, Evidence, LicenseRequirements, EventLog, KV, LatestSyncedBlock, \
    BlockchainState


def get_display_state_license(instance: License):
    if instance.state == BlockchainState.REVOKED:
        return "REVOKED"
    ts = int(time.time())
    if instance.end_date < ts:
        return "EXPIRED"
    elif instance.state == BlockchainState.REGISTERED:
        return "REGISTERED"
    return ""


def get_display_state_requirement(instance: LicenseRequirements):
    parent_state = get_display_state_license(instance.license_obj)
    if instance.state == BlockchainState.REVOKED:
        return instance.state
    if parent_state == BlockchainState.REGISTERED:
        return instance.state
    return parent_state


def get_display_state_evidence(instance: Evidence):
    parent_state = get_display_state_requirement(instance.requirement_obj)
    if instance.state == BlockchainState.REVOKED:
        return instance.state
    if parent_state == BlockchainState.REGISTERED:
        return instance.state
    return parent_state


class LatestSyncedBlockNode(DjangoObjectType):
    class Meta:
        model = LatestSyncedBlock
        fields = ("last_synced_block_number", "id")


class LicenseProductNode(DjangoObjectType):
    class Meta:
        model = LicenseProduct
        interfaces = (graphene.relay.Node,)
        fields = ("id", "name", "license_address", "requirement_address", "kv_address")

    @classmethod
    def get_node(cls, info, id):
        return LicenseProduct.objects.get(id=id)


class LicenseProductConnection(graphene.relay.Connection):
    class Meta:
        node = LicenseProductNode

    total_count = graphene.Int()

    def resolve_total_count(root, info):
        return len(root.iterable)


class KVNode(DjangoObjectType):
    class Meta:
        model = KV
        interfaces = (graphene.relay.Node,)
        fields = ("id", "tx", "timestamp", "key", "value")


class EvidenceNode(DjangoObjectType):
    state = graphene.String()

    class Meta:
        model = Evidence
        interfaces = (graphene.relay.Node,)
        fields = ("id", "evidence_id", "tx", "timestamp", "license_id", "requirement_id",
                  "product", "additional_data", "additional_data_kv", "evidence_kv", "requirement_obj")

    def resolve_state(self, info):
        return get_display_state_evidence(self)


class EvidenceConnection(graphene.relay.Connection):
    class Meta:
        node = EvidenceNode

    total_count = graphene.Int()

    def resolve_total_count(root, info):
        return len(root.iterable)


class RequirementNode(DjangoObjectType):
    evidences = graphene.List(EvidenceNode)
    state = graphene.String()

    class Meta:
        model = LicenseRequirements
        interfaces = (graphene.relay.Node,)
        fields = ("id", "tx", "timestamp", "requirement_id", "requirement_name", "evidences",
                  "license_id", "product", "additional_data", "additional_data_kv", "license_obj")

    def resolve_evidences(self, info):
        return Evidence.objects.filter(requirement_id=self.requirement_id,
                                       license_id=self.license_id,
                                       product__id=self.product.id,
                                       state=BlockchainState.REGISTERED)

    def resolve_state(self, info):
        return get_display_state_requirement(self)


class RequirementConnection(graphene.relay.Connection):
    class Meta:
        node = RequirementNode

    total_count = graphene.Int()

    def resolve_total_count(root, info):
        return len(root.iterable)


class LicenseNode(DjangoObjectType):
    requirements = graphene.relay.ConnectionField(RequirementConnection)
    state = graphene.String()

    class Meta:
        model = License
        interfaces = (graphene.relay.Node,)
        fields = ("id", "tx", "license_id", "license_name", "owner_id", "owner_name",
                  "start_date", "end_date", "additional_data", "timestamp", "product", "additional_data_json",
                  "additional_data_kv")

    def resolve_requirements(self, info, first=0, last=0, before=None, after=None):
        return LicenseRequirements.objects.filter(license_id=self.license_id, product__id=self.product.id)

    def resolve_state(self, info):
        return get_display_state_license(self)


class LicenseConnection(graphene.relay.Connection):
    class Meta:
        node = LicenseNode

    total_count = graphene.Int()

    def resolve_total_count(root, info):
        return len(root.iterable)


class LogNode(DjangoObjectType):
    class Meta:
        model = EventLog
        interfaces = (graphene.relay.Node,)
        fields = ("id", "tx", "timestamp", "license_id", "license_name", "owner_id", "owner_name",
                  "start_date", "end_date", "additional_data", "additional_data_kv", "timestamp", "log_type",
                  "requirement_id", "requirement_name", "evidence_id", "key", "value")


class LogConnection(graphene.relay.Connection):
    class Meta:
        node = LogNode

    total_count = graphene.Int()

    def resolve_total_count(root, info):
        return len(root.iterable)


class QueryProducts(graphene.ObjectType):
    products = graphene.relay.ConnectionField(LicenseProductConnection, search=graphene.String(required=False))
    product = graphene.Field(LicenseProductNode, license_address=graphene.String())

    def resolve_products(root, info, search='', first=0, last=0, before=None, after=None):
        if search is not None and search != '':
            query = LicenseProduct.objects.filter(
                Q(name__icontains=search) | Q(license_address__iexact=search)
                | Q(requirement_address__iexact=search)
                | Q(kv_address__iexact=search)
            )
        else:
            query = LicenseProduct.objects
        return query.filter(is_active=True).order_by('created_at')

    def resolve_product(self, info, license_address):
        try:
            return LicenseProduct.objects.get(license_address=license_address, is_active=True)
        except LicenseProduct.DoesNotExist:
            return None


class QueryLicenses(graphene.ObjectType):
    licenses = graphene.relay.ConnectionField(LicenseConnection, license_address=graphene.String(),
                                              search=graphene.String(required=False))
    license = graphene.Field(LicenseNode, license_address=graphene.String(), license_id=graphene.String())

    def resolve_licenses(self, info, license_address, search='', first=0, last=0, before=None, after=None):
        # We can easily optimize query count in the resolve method
        if search is not None and search != '':
            query = License.objects.filter(
                Q(license_id__icontains=search) |
                Q(license_name__icontains=search) |
                Q(owner_id__iexact=search) |
                Q(owner_name__icontains=search) |
                Q(tx__iexact=search)
            )
        else:
            query = License.objects
        return query.filter(product__license_address=license_address).order_by('-created_at')

    def resolve_license(self, info, license_address, license_id):
        try:
            return License.objects.get(product__license_address=license_address, license_id=license_id)
        except License.DoesNotExist:
            return None


class QueryRequirements(graphene.ObjectType):
    requirements = graphene.relay.ConnectionField(RequirementConnection,
                                                  license_address=graphene.String(), license_id=graphene.String())

    def resolve_requirements(self, info, license_address, license_id, first=0, last=0, before=None, after=None):
        return LicenseRequirements.objects.filter(product__license_address=license_address,
                                                  license_id=license_id)


class EvidenceDetailNode(graphene.ObjectType):
    evidences = graphene.relay.ConnectionField(EvidenceConnection, license_type=graphene.String(),
                                               search=graphene.String(required=False))
    # requirements = graphene.List(RequirementNode, license_id=graphene.String(required=True))
    logs = graphene.relay.ConnectionField(LogConnection, from_ts=graphene.Int(), to_ts=graphene.Int(),
                                          log_type=graphene.String())

    def resolve_evidences(self, info, license_type='', search='', first=0, last=0, before=None, after=None):
        if self['evidence_id'] is None or self['evidence_id'] == '':
            return []
        query = Evidence.objects.filter(product__license_address=self['license_address'],
                                        evidence_id=self['evidence_id'])

        ts = int(time.time())
        if license_type == 'REGISTERED':
            query = query.filter(
                state=BlockchainState.REGISTERED,
                requirement_obj__state=BlockchainState.REGISTERED,
                requirement_obj__license_obj__state=BlockchainState.REGISTERED,
                requirement_obj__license_obj__end_date__gte=ts)
        if license_type == 'REVOKED':
            query = query.filter(
                Q(state=BlockchainState.REVOKED) | Q(requirement_obj__state=BlockchainState.REVOKED) | Q(
                    requirement_obj__license_obj__state=BlockchainState.REVOKED) | Q(
                    requirement_obj__license_obj__end_date__lt=ts)
            )
        if search is not None and search != '':
            query = query.filter(
                Q(license_id__icontains=search) |
                Q(requirement_obj__license_obj__owner_id__icontains=search) |
                Q(requirement_obj__license_obj__owner_name__icontains=search)
            )
        return query

    def resolve_logs(self, info, from_ts=0, to_ts=0, log_type='', first=0, last=0, before=None, after=None):
        if self['evidence_id'] is None or self['evidence_id'] == '':
            return []
        query = EventLog.objects.filter(product__license_address=self['license_address'],
                                        evidence_id=self['evidence_id'])
        if from_ts > 0:
            query = query.filter(timestamp__gte=from_ts)
        if to_ts > 0:
            query = query.filter(timestamp__lte=to_ts)
        if log_type != '':
            query = query.filter(log_type=log_type)
        return query.order_by('-timestamp')


class QueryEvidences(graphene.ObjectType):
    evidence = graphene.Field(EvidenceDetailNode, license_address=graphene.String(required=True),
                              evidence_id=graphene.String(required=True))

    def resolve_evidence(self, info, license_address, evidence_id):
        return {'license_address': license_address, 'evidence_id': evidence_id}


class Query(QueryProducts, QueryLicenses, QueryRequirements, QueryEvidences):
    logs = graphene.relay.ConnectionField(LogConnection, license_address=graphene.String(required=True),
                                          license_id=graphene.String(required=True),
                                          from_ts=graphene.Int(), to_ts=graphene.Int(), log_type=graphene.String())
    kv = graphene.Field(KVNode, license_address=graphene.String(required=True), key=graphene.String(required=True))
    last_synced_block_number = graphene.Field(LatestSyncedBlockNode)

    def resolve_logs(self, info, license_address, license_id, from_ts=0, to_ts=0, log_type='',
                     first=0, last=0, before=None, after=None):
        query = EventLog.objects.filter(product__license_address=license_address) \
            .filter(license_id=license_id)
        if from_ts > 0:
            query = query.filter(timestamp__gte=from_ts)
        if to_ts > 0:
            query = query.filter(timestamp__lte=to_ts)
        if log_type != '':
            query = query.filter(log_type=log_type)
        return query.order_by('-timestamp')

    def resolve_last_synced_block_number(self, info):
        return LatestSyncedBlock.objects.first()

    def resolve_kv(self, info, license_address, key):
        return KV.objects.get(product__license_address=license_address, key=key)


schema = graphene.Schema(query=Query)
