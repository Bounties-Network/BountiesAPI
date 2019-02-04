import user.schema
import graphene

from graphene_django.debug import DjangoDebug


class Query(user.schema.Query,
            graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')
    pass


schema = graphene.Schema(query=Query)
