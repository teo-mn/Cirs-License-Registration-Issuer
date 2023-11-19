import graphene
from graphene_django import DjangoObjectType

from license_registration_issuer.models import EventLog


class TestType(DjangoObjectType):
    class Meta:
        model = EventLog
        fields = ("id", "tx", "log_type")


class Query(graphene.ObjectType):
    all_test = graphene.List(TestType)

    def resolve_all_test(root, info):
        # We can easily optimize query count in the resolve method
        return EventLog.objects.all()


schema = graphene.Schema(query=Query)
