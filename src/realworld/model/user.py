from datetime import datetime, timedelta

from protean.core.field.basic import DateTime, String

from realworld.domain import domain
from realworld.lib.jwt import generate_token


@domain.data_transfer_object
class UserRegistrationDTO:
    email = String(required=True, max_length=250)
    username = String(required=True, max_length=50)
    password = String(required=True, max_length=255)


@domain.aggregate
class User:
    email = String(required=True, max_length=250)
    username = String(required=True, max_length=50)
    password = String(required=True, max_length=255)
    bio = String(max_length=1024)
    token = String(max_length=1024)
    token_valid_until = DateTime()

    @classmethod
    def register(self, user_dto: UserRegistrationDTO):
        return User(email=user_dto.email, username=user_dto.username, password=user_dto.password)

    def authenticate(self, password: str):
        return password == self.password

    def refresh_token(self):
        token = generate_token(self.id)

        self.token = token
        self.token_valid_until = datetime.now() + timedelta(days=1)
