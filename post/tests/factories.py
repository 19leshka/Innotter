import factory

from innotter.utils.tests.base import faker

from post.models import Post
from page.tests.factories import PageFactory
from user.tests.factories import UserFactory


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    content = factory.LazyAttribute(lambda _: faker.name())
    page = factory.SubFactory(PageFactory)
    owner = factory.SubFactory(UserFactory)

