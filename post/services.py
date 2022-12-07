from django.http import HttpRequest

from post.models import Post


class PostServices:
    @staticmethod
    def like_unlike_switch(post: Post, request: HttpRequest) -> dict:
        if request.user not in post.liked_by.all():
            post.liked_by.add(request.user)
            message = {'status': 'You like this post'}

        else:
            post.liked_by.remove(request.user)
            message = {'status': 'You don\'t like this post anymore'}

        return message
