from enum import Enum


class Status(Enum):
    active = 1
    inactive = 2

    @classmethod
    def has_value(cls, value: int) -> bool:
        return value in [item.value for item in cls]

