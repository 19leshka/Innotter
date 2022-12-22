from unittest import TestCase
from user.services import UserService
from user.tests.factories import UserFactory


class TestPageService(TestCase):
    def test_put_item(self):
        user1 = UserFactory()
        result1 = UserService.block_unblock_switch(user1.id)
        self.assertEqual(result1, {'status': 'User is blocked'})

        result2 = UserService.block_unblock_switch(user1.id)
        self.assertEqual(result2, {'status': 'User is unblocked'})
