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
    label: str
    count: int


class SubgroupPydantic(SubgroupBasePydantic):
    id: int
    group_id: int

    class Config:
        orm_mode = True


class SubgroupInCreatePydantic(SubgroupBasePydantic):
    pass


class SubgroupInUpdatePydantic(SubgroupBasePydantic):
    pass
