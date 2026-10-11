from datetime import datetime

import strawberry
from core.constants import ProjectVisibility, RenderStatus
from schemas.file import FileResponse
from schemas.project import (
    ProjectWithRenderFileFullResponse,
    ProjectResponseList,
    ProjectResponse,
)
from schemas.render import RenderWithFileFullResponse
from schemas.tag import TagResponse, TagResponseList
from schemas.user import UserFullResponse, UserResponse


@strawberry.type
class UserType:
    id: int
    surname: str
    name: str
    username: str
    registration_date: datetime

    @classmethod
    def from_dto(cls, user: UserResponse) -> "UserType":
        return cls(**user.model_dump())


@strawberry.type
class FileType:
    id: int
    name: str
    size: int

    @classmethod
    def from_dto(cls, file: FileResponse) -> "FileType":
        return cls(**file.model_dump())


@strawberry.type
class RenderType:
    width: int
    height: int
    samples: int
    denoiser: bool
    gpu: bool
    id: int

    file_id: int
    url: str | None
    file: FileType | None

    @classmethod
    def from_dto(cls, render: RenderWithFileFullResponse) -> "RenderType":
        file_type = FileType.from_dto(render.file)
        return cls(**render.model_dump(exclude={"file"}), file=file_type)


@strawberry.type
class ProjectType:
    id: int
    user_id: int
    render_id: int | None
    name: str
    description: str
    source_file_id: int
    visibility: ProjectVisibility
    status: RenderStatus

    @classmethod
    def from_dto(cls, project: ProjectWithRenderFileFullResponse) -> "ProjectType":
        render_type = RenderType.from_dto(project.render)
        return cls(**project.model_dump(exclude={"render"}), render=render_type)

    @classmethod
    def from_response_dto(cls, project: ProjectResponse) -> "ProjectType":
        return cls(**project.model_dump())


@strawberry.type
class ProjectsType:
    project_list: list[ProjectType]
    size: int
    page: int

    @classmethod
    def from_dto(cls, project_response_list: ProjectResponseList) -> "ProjectsType":
        project_list = []
        for project in project_response_list.project_list:
            project_type = ProjectType.from_response_dto(project)
            project_list.append(project_type)
        return cls(
            project_list=project_list,
            size=project_response_list.size,
            page=project_response_list.page,
        )


@strawberry.type
class TagType:
    id: int
    name: str
    project_id: int

    @classmethod
    def from_dto(cls, tag: TagResponse) -> "TagType":
        return cls(**tag.model_dump())


@strawberry.type
class TagListType:
    tag_list: list[TagType] | None

    @classmethod
    def from_dto(cls, tag_response_list: TagResponseList) -> "TagListType":
        tag_list = []
        for tag in tag_response_list.tag_list:
            tag_type = TagType.from_dto(tag)
            tag_list.append(tag_type)
        return cls(
            tag_list=tag_list,
        )
