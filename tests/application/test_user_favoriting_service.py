import pytest

from realworld.application_services.command.favorite_article_command import FavoriteArticleCommand
from realworld.application_services.command.unfavorite_article_command import UnfavoriteArticleCommand
from realworld.application_services.command.user_authentication_command import UserAuthenticationCommand
from realworld.application_services.user_authentication_service import UserAuthenticationService
from realworld.application_services.user_favoriting_service import UserFavoritingService
from realworld.model.article import Article
from realworld.model.user import User


class TestUserFavoritingService:
    @pytest.fixture
    def user1(self, test_domain):
        user_dao = test_domain.get_dao(User)
        return user_dao.create(email='john.doe@gmail.com', username='john.doe', password='secret1')

    @pytest.fixture
    def user2(self, test_domain):
        user_dao = test_domain.get_dao(User)
        return user_dao.create(email='jane.doe@gmail.com', username='jane.doe', password='secret2')

    @pytest.fixture
    def article(self, user2, test_domain):
        article_dao = test_domain.get_dao(Article)
        article = article_dao.create(
            title="How to train your dragon",
            slug="how-to-train-your-dragon",
            description="Ever wonder how?",
            body="You have to believe",
            tag_list=["reactjs", "angularjs", "dragons"],
            author=user2
        )

        return article

    def test_successful_article_favoriting(self, user1, user2, article):
        auth_command = UserAuthenticationCommand(email=user1.email, password=user1.password)
        authenticated_user = UserAuthenticationService.authenticate_user(auth_command)

        favorite_command = FavoriteArticleCommand(token=authenticated_user['token'], slug=article.slug)
        article_resource = UserFavoritingService.favorite_article(favorite_command)

        assert article_resource is not None
        assert article_resource['slug'] == article.slug
        assert article_resource['favorited'] is True

    def test_successful_article_unfavoriting(self, user1, user2, article):
        auth_command = UserAuthenticationCommand(email=user1.email, password=user1.password)
        authenticated_user = UserAuthenticationService.authenticate_user(auth_command)

        favorite_command = FavoriteArticleCommand(token=authenticated_user['token'], slug=article.slug)
        article_resource = UserFavoritingService.favorite_article(favorite_command)

        assert article_resource is not None
        assert article_resource['slug'] == article.slug
        assert article_resource['favorited'] is True

        unfavorite_command = UnfavoriteArticleCommand(token=authenticated_user['token'], slug=article.slug)
        article_resource = UserFavoritingService.unfavorite_article(unfavorite_command)

        assert article_resource is not None
        assert article_resource['slug'] == article.slug
        assert article_resource['favorited'] is False
