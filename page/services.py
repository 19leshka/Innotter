from django.http import HttpRequest

from innotter.enum import MessageType
from innotter.producer import producer
from page.models import Page


class PageService:
    @staticmethod
    def follow_unfollow_switch(pk: int, request: HttpRequest) -> dict:
        page = Page.objects.get(pk=pk)
        if request.user not in page.followers.all():
            if page.is_private:
                page.follow_requests.add(request.user)
                message = {'status': 'Follow request created'}
            else:
                page.followers.add(request.user)
                message = {'status': 'You follow this page'}
                producer({'id': pk, 'count': 1, 'type': MessageType.ADD_FOLLOWER.value})
        else:
            page.followers.remove(request.user)
            message = {'status': 'You unfollow this page'}
            producer({'id': pk, 'count': 1, 'type': MessageType.DEL_FOLLOWER.value})
        return message

    @staticmethod
    def block_unblock_switch(user_id: int):
        page = Page.objects.get(pk=user_id)
        if page.is_blocked:
            page.is_blocked = False
            message = {'status': 'Page is unblocked'}
        else:
            page.is_blocked = True
            message = {'status': 'Page is blocked'}
        page.save()
        return message
