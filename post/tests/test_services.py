from unittest import TestCase
from unittest.mock import patch

import pytest

from post.services import PostServices


class TestPageServiceMock(TestCase):
    @pytest.mark.django_db
    @patch('page.services.PostServices.like_unlike_switch')
    def test_put_item(self, mock_like_unlike_switch):
        test_cases = (
            {
                'expected': {'status': 'You like this post'}
            },
            {
                'expected': {'status': 'You don\'t like this post anymore'}
            },
        )

        for test_case in test_cases:
            mock_like_unlike_switch.return_value = test_case['expected']
            result = PostServices.like_unlike_switch({}, {})
            self.assertEqual(result, test_case['expected'])