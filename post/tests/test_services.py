from django.test import RequestFactory, TestCase

from post.tests.factories import PostFactory
from post.services import PostServices
from user.tests.factories import UserFactory


class TestPostService(TestCase):
    def setUp(self):
        self.post1 = PostFactory()
        self.user1 = UserFactory()
    def test_put_item(self):
        test_cases = (
            {
                'expected': {'status': 'You like this post'}
            },
            {
                'expected': {'status': 'You don\'t like this post anymore'}
            },
        )

        request = RequestFactory().get('/post')
        request.user = self.user1

        for test_case in test_cases:
            result = PostServices.like_unlike_switch(self.post1, request)
            self.assertEqual(result, test_case['expected'])
