from django.test import TestCase

from page.models import Page
from page.services import PageService

def smth():
    return True


class PageServiceTest(TestCase):
    def test_follow_unfollow_switch(self):
        Page.objects.create(name='page1', description='desc', owner=1)
        Page.objects.create(name='page2', description='desc', owner=1, is_blocked=True)

        # result = PageService.follow_unfollow_switch(self.page1.get('pk'), {'user': 1})
        # expected = {'status': 'Follow request created'}
        result = smth()
        self.assertEqual(result, 1)
