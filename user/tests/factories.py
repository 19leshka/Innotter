import factory

from innotter.utils.tests.base import faker

from user.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: faker.name())
    email = factory.LazyAttribute(lambda _: faker.unique.email())
    password = factory.LazyAttribute(lambda _: faker.password())
