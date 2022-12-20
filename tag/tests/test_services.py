from unittest import TestCase
from unittest.mock import patch

from tag.services import TagService


class TestPageServiceMock(TestCase):
    @patch('tag.services.TagService.process_tags')
    def test_put_item(self, mock_process_tags):
        test_cases = (
            {
                'expected': [1,2,3],
                'arguments': ['sport', 'games', 'news']
            },
            {
                'expected': [2,3],
                'arguments': ['games', 'news']
            },
            {
                'expected': [1,4],
                'arguments': ['sport', 'movies']
            },
        )

        for test_case in test_cases:
            mock_process_tags.return_value = test_case['expected']
            result = TagService.process_tags({'data': {'tags': test_case['arguments']}})
            self.assertEqual(result, test_case['expected'])