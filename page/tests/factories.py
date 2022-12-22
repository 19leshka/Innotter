import factory

from innotter.utils.tests.base import faker

from page.models import Page
from user.tests.factories import UserFactory


class PageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Page

    name = factory.LazyAttribute(lambda _: faker.name())
    description = factory.LazyAttribute(lambda _: faker.name())
    owner = factory.SubFactory(UserFactory)

