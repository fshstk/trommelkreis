from graphene_django import DjangoObjectType
import graphene

import archive.models


class Challenge(DjangoObjectType):
    class Meta:
        model = archive.models.Challenge
        fields = ("id", "name", "blurb", "description")


class Session(DjangoObjectType):
    class Meta:
        model = archive.models.Session
        fields = ("id", "slug", "date", "challenge")


class Artist(DjangoObjectType):
    class Meta:
        model = archive.models.Artist
        fields = ("id", "name")


class AudioFile(DjangoObjectType):
    class Meta:
        model = archive.models.AudioFile
        fields = ("id", "name", "artist")


class Query(graphene.ObjectType):
    sessions = graphene.List(Session)
    session_by_slug = graphene.Field(Session, slug=graphene.String(required=True))

    def resolve_sessions(self, info):
        return archive.models.Session.objects.all()

    def resolve_session_by_slug(self, info, slug):
        try:
            return archive.models.Session.objects.get(slug=slug)
        except archive.models.Session.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)