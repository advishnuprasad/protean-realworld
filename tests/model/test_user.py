import pytest

from uuid import UUID

from protean.core.exceptions import ValidationError

from realworld.model.user import User, UserRegistrationDTO


class TestUser:
    def test_that_user_can_be_initialized_successfully(self):
        user = User(email='jake@jake.jake', username='jake', password='nopass')
        assert user is not None

    def test_that_mandatory_fields_are_validated(self):
        with pytest.raises(ValidationError):
            User()

    def test_that_a_new_user_can_be_registered_successfully(self):
        user_dto = UserRegistrationDTO(email='jake@jake.jake', username='jake', password='nopass')

        user = User.register(user_dto)

        assert user is not None
        assert isinstance(user, User)
        assert user.id is not None

        try:
            UUID(str(user.id))
        except ValueError:
            pytest.fail("ID is not valid UUID")

    def test_successful_password_authentication(self):
        user = User(email='jake@jake.jake', username='jake', password='nopass')

        assert user.authenticate('nopass') is True

    def test_unsuccessful_password_authentication(self):
        user = User(email='jake@jake.jake', username='jake', password='nopass')

        assert user.authenticate('wrongpass') is False
