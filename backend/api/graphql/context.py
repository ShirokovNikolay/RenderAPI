from functools import cached_property
from typing import Annotated

from fastapi import Depends
from infrastructure.database.core import get_session
from infrastructure.database.unit_of_work import UnitOfWork
from services.auth import AuthService
from services.projects.project import ProjectService
from services.projects.project_access_validator import ProjectAccessValidatorService
from services.projects.project_pagination import ProjectPaginationService
from services.tag import TagService
from services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import BaseContext


class Context(BaseContext):
    def __init__(
        self,
        session: AsyncSession,
        user_id: int | None = None,
    ) -> None:
        super().__init__()
        self.session = session
        self.user_id = user_id

    @cached_property
    def unit_of_work(self) -> UnitOfWork:
        return UnitOfWork(self.session)

    @cached_property
    def auth_service(self) -> AuthService:
        return AuthService(unit_of_work=self.unit_of_work)

    @cached_property
    def user_service(self) -> UserService:
        return UserService(unit_of_work=self.unit_of_work)

    @cached_property
    def project_service(self) -> ProjectService:
        return ProjectService(
            unit_of_work=self.unit_of_work,
            project_access_validator=self.project_access_validator,
        )

    @cached_property
    def project_pagination_service(self) -> ProjectPaginationService:
        return ProjectPaginationService(unit_of_work=self.unit_of_work)

    @cached_property
    def project_access_validator(self) -> ProjectAccessValidatorService:
        return ProjectAccessValidatorService(unit_of_work=self.unit_of_work)

    @cached_property
    def tag_service(self) -> TagService:
        return TagService(unit_of_work=self.unit_of_work)


async def get_context(
    session: Annotated[
        AsyncSession,
        Depends(get_session),
    ],
) -> Context:
    return Context(session=session)
