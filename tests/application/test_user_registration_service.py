from realworld.application.command.user_registration_command import UserRegistrationCommand
from realworld.application.user_registration_service import UserRegistrationService


class TestUserRegistrationService:
    def test_successful_user_creation(self, test_domain):
        command = UserRegistrationCommand(
            email='jake@jake.jake', username='jake', password='nopass'
            )

        user_resource = UserRegistrationService.register_user(command)
        assert user_resource is not None
