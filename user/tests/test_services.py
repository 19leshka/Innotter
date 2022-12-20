from unittest import TestCase
from unittest.mock import patch

from user.services import UserService


class TestPageServiceMock(TestCase):
    @patch('tag.services.UserService.block_unblock_switch')
    def test_put_item(self, mock_block_unblock_switch):
        test_cases = (
            {
                'expected': {'status': 'User is unblocked'},
                'arguments': 1
            },
            {
                'expected': {'status': 'User is blocked'},
                'arguments': 1
            }
        )

        for test_case in test_cases:
            mock_block_unblock_switch.return_value = test_case['expected']
            result = UserService.block_unblock_switch(test_case['arguments'])
            self.assertEqual(result, test_case['expected'])