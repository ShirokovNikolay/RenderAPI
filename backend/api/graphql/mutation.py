import strawberry
from strawberry import Info

from api.graphql.context import Context
from api.graphql.graphql_types.input import TagInput
from api.graphql.graphql_types.query import TagType


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_tag(
        self, info: Info[Context], tag_input: TagInput, user_id: int,
    ) -> TagType:
        unit_of_work = info.context.unit_of_work
        tag_service = info.context.tag_service
        tag_create_data = tag_input.to_dto
        tag_response = await tag_service.create_tag(tag_create_data, user_id)

        await unit_of_work.commit()
        return TagType.from_dto(tag_response)

    @strawberry.mutation
    async def delete_tag(self, info: Info[Context], tag_id: int, user_id: int) -> None:
        unit_of_work = info.context.unit_of_work
        tag_service = info.context.tag_service
        await tag_service.delete_by_id(tag_id, user_id)
        await unit_of_work.commit()
