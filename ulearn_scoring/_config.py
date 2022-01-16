from typing import List

from pydantic import BaseModel
from pydantic import FilePath
from pydantic_yaml import VersionedYamlModel


class Statement(BaseModel):
    file: FilePath
    modules: List[str]


class StatementsConfig(VersionedYamlModel):
    statements: List[Statement]

    class Config:
        min_version = '1.0.0'
        max_version = '2.0.0'
