from user.models import User


class UserService:
    @staticmethod
    def block_unblock(user_id: int):
        user = User.objects.get(pk=user_id)
        if user.is_blocked:
            user.is_blocked = False
            message = {'status': 'User is unblocked'}
        else:
            user.is_blocked = True
            message = {'status': 'User is blocked'}
        user.save()
        return message
