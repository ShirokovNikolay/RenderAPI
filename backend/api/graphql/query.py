import strawberry

from api.graphql.context import Context
from api.graphql.mock_services import MockS3Client
from api.graphql.schemas import ProjectType, TagListType, UserType, ProjectsType


@strawberry.type
class Query:
    @strawberry.field
    async def user(
        self,
        info: strawberry.Info[Context],
        user_id: int,
    ) -> UserType:
        user_service = info.context.user_service
        user_response = await user_service.get_by_id(user_id)
        return UserType.from_dto(user_response)

    @strawberry.field
    async def project(
        self,
        info: strawberry.Info[Context],
        project_id: int,
        user_id: int,
    ) -> ProjectType:
        project_service = info.context.project_service
        s3_client = MockS3Client()
        project = await project_service.get_by_id(project_id, user_id, s3_client)
        return ProjectType.from_dto(project)

    @strawberry.field
    async def projects(
        self,
        info: strawberry.Info[Context],
    ) -> ProjectsType:
        project_pagination_service = info.context.project_pagination_service
        projects = await project_pagination_service.get_public_projects(
            size=10,
            page=1,
        )
        return ProjectsType.from_dto(projects)

    @strawberry.field
    async def project_tags(
        self,
        info: strawberry.Info[Context],
        project_id: int,
        user_id: int,
    ) -> TagListType:
        tag_service = info.context.tag_service
        tag_response_list = await tag_service.get_project_tags(project_id, user_id)
        return TagListType.from_dto(tag_response_list)
