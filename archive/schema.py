from graphene_django import DjangoObjectType
import graphene

from archive.models import Challenge, Session, Artist, AudioFile

base_link = "https://trommelkreis.club"


class ChallengeType(DjangoObjectType):
    class Meta:
        model = Challenge
        fields = ("name", "blurb", "description")


class SessionType(DjangoObjectType):
    url = graphene.String()

    def resolve_url(parent, info):
        # TODO: do this properly
        return f"{base_link}/archiv/sessions/{parent.slug}/"

    class Meta:
        model = Session
        fields = ("slug", "date", "challenge", "tracks")


class AudioFileType(DjangoObjectType):
    duration = graphene.String()
    url = graphene.String()
    artist = graphene.String()

    def resolve_url(parent, info):
        return parent.url

    def resolve_duration(parent, info):
        # TODO: this is defined multiple times now. refactor as model property!
        return "{:02d}:{:02d}".format(parent.duration // 60, parent.duration % 60)

    def resolve_artist(parent, info):
        return parent.artist.name if parent.artist is not None else "(Anonym)"

    class Meta:
        model = AudioFile
        fields = ("name", "id", "session_subsection")


class Query(graphene.ObjectType):
    sessions = graphene.List(SessionType)
    session = graphene.Field(SessionType, slug=graphene.String(required=True))

    def resolve_sessions(self, info):
        return Session.objects.all()

    def resolve_session(self, info, slug):
        try:
            return Session.objects.get(slug=slug)
        except Session.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)
