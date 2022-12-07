from page.models import Page
from user.models import User


class UserService:
    @staticmethod
    def block_unblock_switch(user_id: int):
        user = User.objects.get(pk=user_id)
        pages = Page.objects.select_related('owner').filter(owner_id=user_id)
        if user.is_blocked:
            user.is_blocked = False
            message = {'status': 'User is unblocked'}
        else:
            user.is_blocked = True
            message = {'status': 'User is blocked'}
        user.save()

        for page in pages:
            if user.is_blocked and not page.is_blocked:
                page.is_blocked = True
            elif not user.is_blocked and page.is_blocked:
                page.is_blocked = False
            page.save()
        return message

