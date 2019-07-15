import factory
from pytest_factoryboy import register

from realworld.model.user import User


@register
class UserFactory(factory.Factory):

    class Meta:
        model = User

    email = factory.Faker('email')
    username = factory.Faker('user_name')
    password = factory.Faker('password')
