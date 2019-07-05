from realworld.application_services.command.user_registration_command import UserRegistrationCommand
from realworld.application_services.user_registration_service import UserRegistrationService
from realworld.model.user import User


class TestUserRegistrationService:
    def test_registering_user_via_user_registration_service(self, test_domain):
        command = UserRegistrationCommand(
            email='jake@jake.jake', username='jake', password='nopass'
            )

        user_resource = UserRegistrationService.register_user(command)
        assert user_resource is not None

    def test_that_user_is_persisted_in_the_registration_service(self, test_domain):
        command = UserRegistrationCommand(
            email='jake@jake.jake', username='jake', password='nopass'
            )

        user_resource = UserRegistrationService.register_user(command)

        # FIXME Should check for this via Repository itself
        user_dao = test_domain.get_dao(User)
        persisted_user = user_dao.get(user_resource.id)
        assert persisted_user is not None
        assert hasattr(persisted_user, 'id')

    def test_that_user_token_is_empty_immediately_after_registration_and_before_authentication(self, test_domain):
        command = UserRegistrationCommand(
            email='jake@jake.jake', username='jake', password='nopass'
            )

        user_resource = UserRegistrationService.register_user(command)
        assert user_resource.token is None
