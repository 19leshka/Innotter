from enum import Enum


class MessageType(Enum):
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'

    def __str__(self):
        return self.value
