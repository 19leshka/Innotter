from unittest import TestCase
from unittest.mock import patch

import pytest

from page.services import PageService


class TestPageServiceMock(TestCase):

    @pytest.mark.django_db
    @patch('page.services.PageService.follow_unfollow_switch')
    def test_put_item(self, mock_follow_unfollow_switch):
        test_cases = (
            {
                'expected': {'status': 'Follow request created'},
                'pk': 0
            },
            {
                'expected': {'status': 'You follow this page'},
                'pk': 1
            },
            {
                'expected': {'status': 'You unfollow this page'},
                'pk': 1
            },
        )

        for test_case in test_cases:
            mock_follow_unfollow_switch.return_value = test_case['expected']
            result = PageService.follow_unfollow_switch(test_case['pk'], {})
            self.assertEqual(result, test_case['expected'])


    @pytest.mark.django_db
    @patch('page.services.PageService.block_unblock_switch')
    def test_put_item(self, mock_block_unblock_switch):
        test_cases = (
            {
                'expected': {'status': 'Page is unblocked'},
                'pk': 1
            },
            {
                'expected': {'status': 'Page is blocked'},
                'pk': 1
            },
        )

        for test_case in test_cases:
            mock_block_unblock_switch.return_value = test_case['expected']
            result = PageService.follow_unfollow_switch(test_case['pk'], {})
            self.assertEqual(result, test_case['expected'])