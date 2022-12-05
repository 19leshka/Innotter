from django.http import HttpRequest

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
        else:
            page.followers.remove(request.user)
            message = {'status': 'You unfollow this page'}
        return message