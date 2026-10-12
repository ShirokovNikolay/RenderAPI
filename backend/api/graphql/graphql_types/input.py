import strawberry
from schemas.tag import TagCreate


@strawberry.input
class TagInput:
    project_id: int
    name: str

    @property
    def to_dto(self) -> TagCreate:
        return TagCreate(
            project_id=self.project_id,
            name=self.name,
        )
