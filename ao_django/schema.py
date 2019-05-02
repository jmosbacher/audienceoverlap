import graphene

import ao_django.audience_manager.schema


class Query(ao_django.audience_manager.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

schema = graphene.Schema(query=Query)