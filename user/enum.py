from enum import Enum


class Roles(Enum):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    @classmethod
    def choices(cls):
        return [(attr.value, attr.name) for attr in cls]

    def __str__(self) -> str:
        return self.value
