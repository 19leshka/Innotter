from django.test import RequestFactory, TestCase
from page.services import PageService
from page.tests.factories import PageFactory
from user.tests.factories import UserFactory


class TestPageService(TestCase):
    def setUp(self):
        self.page1 = PageFactory()
        self.user1 = UserFactory()

    def test_follow_unfollow(self):
        request = RequestFactory().get('/pages')
        request.user = self.user1

        test_cases = (
            {
                'expected': {'status': 'You follow this page'},
                'pk': self.page1.pk
            },
            {
                'expected': {'status': 'You unfollow this page'},
                'pk': self.page1.pk
            },
        )

        for test_case in test_cases:
            result = PageService.follow_unfollow_switch(test_case['pk'], request)
            self.assertEqual(result, test_case['expected'])

        self.page1.is_private = True
        self.page1.save()
        result = PageService.follow_unfollow_switch(self.page1.pk, request)
        self.assertEqual(result, {'status': 'Follow request created'})

    def test_block_unblock(self):
        test_cases = (
            {
                'expected': {'status': 'Page is blocked'},
                'pk': self.page1.pk
            },
            {
                'expected': {'status': 'Page is unblocked'},
                'pk': self.page1.pk
            },
        )

        for test_case in test_cases:
            result = PageService.block_unblock_switch(test_case['pk'])
            self.assertEqual(result, test_case['expected'])
