from protean.core.field.basic import String

from realworld.domain import domain


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

    @classmethod
    def register_user(self, user_dto: UserRegistrationDTO):
        return User(email=user_dto.email, username=user_dto.username, password=user_dto.password)
