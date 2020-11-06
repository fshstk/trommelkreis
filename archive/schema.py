from graphene_django import DjangoObjectType
import graphene

import archive.models


class Session(DjangoObjectType):
    class Meta:
        model = archive.models.Session


class Query(graphene.ObjectType):
    sessions = graphene.List(Session)

    def resolve_sessions(self, info):
        return archive.models.Session.objects.all()


schema = graphene.Schema(query=Query)