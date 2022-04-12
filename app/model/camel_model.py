from pydantic import BaseModel
from humps import camel


def to_camel(string):
    return camel.case(string)


class HashableModel(BaseModel):
    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


class CamelModel(HashableModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
