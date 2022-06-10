from pydantic import BaseModel


class GroupBasePydantic(BaseModel): # noqa
    label: str
    count: int


class GroupPydantic(GroupBasePydantic):
    id: int

    class Config:
        orm_mode = True


class GroupInCreatePydantic(GroupBasePydantic):
    pass


class GroupInUpdatePydantic(GroupBasePydantic):
    pass


class SubgroupBasePydantic(BaseModel):
    count: int


class SubgroupPydantic(SubgroupBasePydantic):
    id: int
    group: GroupPydantic

    class Config:
        orm_mode = True


class SubgroupInCreatePydantic(SubgroupBasePydantic):
    group_id: int


class SubgroupInUpdatePydantic(SubgroupBasePydantic):
    pass


class SubgroupFilterPydantic(BaseModel):
    group_id: int | None = None
