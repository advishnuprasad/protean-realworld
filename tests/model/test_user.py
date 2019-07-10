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

    def test_successfully_updating_a_users_attributes(self):
        user = User(email='jake@jake.jake', username='jake', password='nopass')
        user.update(email='jane@jane.jane')

        assert user.email == 'jane@jane.jane'
        assert user.username == 'jake'

    def test_that_invalid_fields_are_ignored(self):
        user = User(email='jake@jake.jake', username='jake', password='nopass')
        user.update(email='jane@jane.jane', foo='bar')

        assert user.email == 'jane@jane.jane'
        assert hasattr(user, 'foo') is False


class TestFollowFunctionality:
    def test_that_user_can_follow_profile(self):
        user1 = User(email='john.doe@gmail.com', username='johndoe', password='secret1')
        user2 = User(email='jane.doe@gmail.com', username='janedoe', password='secret2')

        updated_user1 = user1.follow(user2)
        assert updated_user1 is not None
        assert isinstance(updated_user1, User)

        assert user2.id in [follow_obj.following.id for follow_obj in updated_user1.follows]

    def test_that_user_cannot_follow_profile_more_than_once(self):
        user1 = User(email='john.doe@gmail.com', username='johndoe', password='secret1')
        user2 = User(email='jane.doe@gmail.com', username='janedoe', password='secret2')

        user1.follow(user2)
        assert len(user1.follows) == 1

        # Following `user2` again should have no effect
        user1 = user1.follow(user2)
        assert len(user1.follows) == 1

    def test_that_user_can_unfollow_profile(self):
        user1 = User(email='john.doe@gmail.com', username='johndoe', password='secret1')
        user2 = User(email='jane.doe@gmail.com', username='janedoe', password='secret2')

        user1.follow(user2)
        assert user2.id in [follow_obj.following.id for follow_obj in user1.follows]

        user1.unfollow(user2)
        assert user2.id not in [follow_obj.following.id for follow_obj in user1.follows]
