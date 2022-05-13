from pydantic import BaseModel


class GroupBasePydantic(BaseModel): # noqa
    label: str
    count: str


class GroupPydantic(GroupBasePydantic):
    id: int

    class Config:
        orm_mode = True


class GroupInCreatePydantic(GroupBasePydantic):
    pass


class GroupInUpdatePydantic(GroupBasePydantic):
    pass


class GroupListPydantic(BaseModel):
    groups: list[GroupPydantic]
    count: int


class SubgroupBasePydantic(BaseModel):
    label: str
    count: str


class SubgroupPydantic(SubgroupBasePydantic):
    id: int
    group_id: int

    class Config:
        orm_mode = True


class SubgroupInCreatePydantic(SubgroupBasePydantic):
    pass


class SubgroupInUpdatePydantic(SubgroupBasePydantic):
    pass


class SubgroupListPydantic(BaseModel):
    subgroups: list[GroupPydantic]
    count: int
