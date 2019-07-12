import pytest

from realworld.application_services.command.create_article_command import CreateArticleCommand
from realworld.application_services.command.user_authentication_command import UserAuthenticationCommand
from realworld.application_services.article_service import ArticleService
from realworld.application_services.user_authentication_service import UserAuthenticationService
from realworld.model.article import Article
from realworld.model.user import User


class TestArticleService:
    @pytest.fixture
    def persisted_user(self, test_domain):
        user_dao = test_domain.get_dao(User)
        user = user_dao.create(email='jake@jake.jake', username='jake', password='nopass')

        return user

    def test_creating_an_article_via_article_service(self, persisted_user, test_domain):
        # Authenticate user to generate valid token
        command = UserAuthenticationCommand(email='jake@jake.jake', password='nopass')
        authenticated_user = UserAuthenticationService.authenticate_user(command)

        command = CreateArticleCommand(
            token=authenticated_user.token,
            title="How to train your dragon",
            description="Ever wonder how?",
            body="You have to believe",
            tag_list=["reactjs", "angularjs", "dragons"]
            )

        article_resource = ArticleService.create_article(command)
        json_dict = article_resource.to_dict()
        assert article_resource is not None

    def test_that_article_is_persisted_in_the_article_service(self, persisted_user, test_domain):
        # Authenticate user to generate valid token
        command = UserAuthenticationCommand(email='jake@jake.jake', password='nopass')
        authenticated_user = UserAuthenticationService.authenticate_user(command)

        command = CreateArticleCommand(
            token=authenticated_user.token,
            title="How to train your dragon",
            description="Ever wonder how?",
            body="You have to believe",
            tag_list=["reactjs", "angularjs", "dragons"]
            )

        article_resource = ArticleService.create_article(command)

        # FIXME Should check for this via Repository itself
        article_dao = test_domain.get_dao(Article)
        persisted_article = article_dao.get(article_resource.id)
        assert persisted_article is not None
        assert hasattr(persisted_article, 'id')
