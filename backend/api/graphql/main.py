import strawberry
from strawberry.fastapi import GraphQLRouter

from api.graphql.context import get_context
from api.graphql.mutation import Mutation
from api.graphql.query import Query

schema = strawberry.Schema(query=Query, mutation=Mutation)

router = GraphQLRouter(
    schema=schema,
    prefix="/graphql",
    context_getter=get_context,
)
