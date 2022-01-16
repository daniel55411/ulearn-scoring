from typing import List

from pydantic import BaseModel
from pydantic import FilePath
from pydantic import validator
from pydantic_yaml import VersionedYamlModel


class Statement(BaseModel):
    file: FilePath
    modules: List[str]

    @validator('file')
    def file_must_be_xlsx(cls, v: FilePath) -> FilePath:
        if not v.name.endswith('xlsx'):
            raise ValueError('file must be xlsx')

        return v


class StatementsConfig(VersionedYamlModel):
    statements: List[Statement]

    class Config:
        min_version = '1.0.0'
        max_version = '2.0.0'
