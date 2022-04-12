from enum import Enum


class Role(Enum):
    user = 1
    admin = 2

    @classmethod
    def has_value(cls, value: int) -> bool:
        return value in [item.value for item in cls]
