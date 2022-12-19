from enum import Enum


class MessageType(Enum):
    CREATE = 'create'
    ADD_LIKE = 'add_like'
    DEL_LIKE = 'del_like'
    ADD_POST = 'add_post'
    DEL_POST = 'del_post'
    ADD_FOLLOWER = 'add_follower'
    DEL_FOLLOWER = 'del_follower'
    DELETE = 'delete'

    def __str__(self):
        return self.value
