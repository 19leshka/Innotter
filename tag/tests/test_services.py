from django.test import RequestFactory, TestCase
from tag.services import TagService


class TestPageService(TestCase):
    def test_put_item(self):
        test_cases = (
            {
                'expected': [1, 2, 3],
                'arguments': ['sport', 'games', 'news'],
            },
            {
                'expected': [2, 3],
                'arguments': ['games', 'news'],
            },
            {
                'expected': [1, 4],
                'arguments': ['sport', 'movies'],
            },
        )

        for test_case in test_cases:
            request = RequestFactory().post(path='/pages', data={'tags': test_case['arguments']})
            result = TagService.process_tags(request)
            self.assertEqual(result, test_case['expected'])
