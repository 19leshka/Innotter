from django.http import HttpRequest

from innotter.enum import MessageType
from innotter.producer import producer
from post.models import Post


class PostServices:
    @staticmethod
    def like_unlike_switch(post: Post, request: HttpRequest) -> dict:
        if request.user not in post.liked_by.all():
            post.liked_by.add(request.user)
            message = {'status': 'You like this post'}
            producer({'id': post.page.id, 'count': 1, 'value': 'total_likes', 'type': MessageType.ADD_LIKE.value})

        else:
            post.liked_by.remove(request.user)
            message = {'status': 'You don\'t like this post anymore'}
            producer({'id': post.page.id, 'count': -1, 'value': 'total_likes', 'type': MessageType.DEL_LIKE.value})

        return message
