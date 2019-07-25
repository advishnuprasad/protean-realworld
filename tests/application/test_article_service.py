import pytest
import random

from datetime import datetime, timedelta

from realworld.application_services.command.create_article_command import CreateArticleCommand
from realworld.application_services.command.delete_article_command import DeleteArticleCommand
from realworld.application_services.command.favorite_article_command import FavoriteArticleCommand
from realworld.application_services.command.get_article_command import GetArticleCommand
from realworld.application_services.command.list_articles_command import ListArticlesCommand
from realworld.application_services.command.update_article_command import UpdateArticleCommand
from realworld.application_services.command.user_authentication_command import UserAuthenticationCommand
from realworld.application_services.article_service import ArticleService
from realworld.application_services.user_authentication_service import UserAuthenticationService
from realworld.application_services.user_favoriting_service import UserFavoritingService
from realworld.model.article import Article
from realworld.model.user import User


class TestArticleService:
    @pytest.fixture
    def persisted_user(self, test_domain):
        user_dao = test_domain.get_dao(User)
        user = user_dao.create(email='jake@jake.jake', username='jake', password='nopass')

        return user

    @pytest.fixture
    def user1(self, test_domain):
        user_dao = test_domain.get_dao(User)
        user = user_dao.create(email='john.doe@gmail.com', username='john.doe', password='nopass1')

        return user

    @pytest.fixture
    def user2(self, test_domain):
        user_dao = test_domain.get_dao(User)
        user = user_dao.create(email='jane.doe@gmail.com', username='jane.doe', password='nopass2')

        return user

    @pytest.fixture
    def persisted_article(self, persisted_user, test_domain):
        article_dao = test_domain.get_dao(Article)
        article = article_dao.create(
            title="How to train your dragon",
            slug="how-to-train-your-dragon",
            description="Ever wonder how?",
            body="You have to believe",
            tag_list=["reactjs", "angularjs", "dragons"],
            author=persisted_user
        )

        return article

    @pytest.fixture
    def persisted_articles(self, user1, user2, test_domain):
        article_dao = test_domain.get_dao(Article)
        tags_list = ["tag{}".format(i) for i in range(1, 25)]

        articles = []
        for counter in range(1, 31):
            tstamp = datetime.now() - timedelta(minutes=30-counter)
            articles.append(
                article_dao.create(
                    title="Article A{}".format(counter),
                    slug="article-a{}".format(counter),
                    description="Article Description for A{}".format(counter),
                    body="Article Body for A{}".format(counter),
                    tag_list=random.sample(tags_list, random.randint(1, 3)),
                    author=random.choice([user1, user2]),
                    created_at=tstamp,
                    updated_at=tstamp
                )
            )

        return articles

    def test_creating_an_article_via_article_service(self, persisted_user, test_domain):
        # Authenticate user to generate valid token
        command = UserAuthenticationCommand(email='jake@jake.jake', password='nopass')
        authenticated_user = UserAuthenticationService.authenticate_user(command)

        command = CreateArticleCommand(
            token=authenticated_user['token'],
            title="How to train your dragon",
            description="Ever wonder how?",
            body="You have to believe",
            tag_list=["reactjs", "angularjs", "dragons"]
            )

        article_resource = ArticleService.create_article(command)
        assert article_resource is not None

    def test_that_article_is_persisted_in_the_article_service(self, persisted_user, test_domain):
        # Authenticate user to generate valid token
        command = UserAuthenticationCommand(email='jake@jake.jake', password='nopass')
        authenticated_user = UserAuthenticationService.authenticate_user(command)

        command = CreateArticleCommand(
            token=authenticated_user['token'],
            title="How to train your dragon",
            description="Ever wonder how?",
            body="You have to believe",
            tag_list=["reactjs", "angularjs", "dragons"]
            )

        article_resource = ArticleService.create_article(command)

        # FIXME Should check for this via Repository itself
        article_dao = test_domain.get_dao(Article)
        persisted_article = article_dao.get(article_resource['id'])
        assert persisted_article is not None
        assert hasattr(persisted_article, 'id')

    def test_that_article_can_be_retrieved_through_the_article_service(self, persisted_article, test_domain):
        command = GetArticleCommand(slug=persisted_article.slug)
        article_resource = ArticleService.get_article(command)

        assert article_resource is not None
        assert article_resource['slug'] == persisted_article.slug

    def test_updating_an_articles_title(self, persisted_article):
        command = UserAuthenticationCommand(email='jake@jake.jake', password='nopass')
        authenticated_user = UserAuthenticationService.authenticate_user(command)

        command = UpdateArticleCommand(
            token=authenticated_user['token'],
            slug=persisted_article.slug,
            title='How to train your dragon - Part 2 - At Worlds End')
        updated_article = ArticleService.update_article(command)
        assert updated_article['slug'] == 'how-to-train-your-dragon-part-2-at-worlds-end'

    def test_deleting_an_article(self, persisted_article):
        command = UserAuthenticationCommand(email='jake@jake.jake', password='nopass')
        authenticated_user = UserAuthenticationService.authenticate_user(command)

        assert ArticleService.get_article(GetArticleCommand(slug=persisted_article.slug)) is not None

        command = DeleteArticleCommand(
            token=authenticated_user['token'],
            slug=persisted_article.slug)
        ArticleService.delete_article(command)

        assert ArticleService.get_article(GetArticleCommand(slug=persisted_article.slug)) is None

    def test_listing_articles_without_query_filters(self, persisted_user, persisted_articles):
        # Authenticate user to generate valid token
        command = UserAuthenticationCommand(email='jake@jake.jake', password='nopass')
        authenticated_user = UserAuthenticationService.authenticate_user(command)

        list_command = ListArticlesCommand(token=authenticated_user['token'])
        article_resources = ArticleService.list_articles(list_command)
        assert len(article_resources) == 20

    def test_listing_articles_without_query_filters_for_reverse_sorted_list(self, persisted_user, persisted_articles):
        # Authenticate user to generate valid token
        command = UserAuthenticationCommand(email='jake@jake.jake', password='nopass')
        authenticated_user = UserAuthenticationService.authenticate_user(command)

        list_command = ListArticlesCommand(token=authenticated_user['token'])
        article_resources = ArticleService.list_articles(list_command)
        assert len(article_resources) == 20
        assert article_resources[0]['slug'] == 'article-a30'

    def test_listing_articles_without_query_filters_with_limit(self, persisted_user, persisted_articles):
        # Authenticate user to generate valid token
        command = UserAuthenticationCommand(email='jake@jake.jake', password='nopass')
        authenticated_user = UserAuthenticationService.authenticate_user(command)

        list_command = ListArticlesCommand(token=authenticated_user['token'], limit=10)
        article_resources = ArticleService.list_articles(list_command)
        assert len(article_resources) == 10
        assert article_resources[0]['slug'] == 'article-a30'

    def test_listing_articles_without_query_filters_with_offset(self, persisted_user, persisted_articles):
        # Authenticate user to generate valid token
        command = UserAuthenticationCommand(email='jake@jake.jake', password='nopass')
        authenticated_user = UserAuthenticationService.authenticate_user(command)

        list_command = ListArticlesCommand(token=authenticated_user['token'], offset=5)
        article_resources = ArticleService.list_articles(list_command)
        assert len(article_resources) == 20
        assert article_resources[0]['slug'] == 'article-a25'

    def test_listing_articles_with_tag_filter(self, persisted_user, persisted_articles):
        # Authenticate user to generate valid token
        command = UserAuthenticationCommand(email='jake@jake.jake', password='nopass')
        authenticated_user = UserAuthenticationService.authenticate_user(command)

        list_command = ListArticlesCommand(token=authenticated_user['token'], tag='tag1')
        article_resources = ArticleService.list_articles(list_command)
        if len(article_resources) > 1:
            assert 'tag1' in article_resources[0]['tag_list']

        list_command = ListArticlesCommand(token=authenticated_user['token'], tag='tag17')
        article_resources = ArticleService.list_articles(list_command)
        if len(article_resources) > 1:
            assert 'tag17' in article_resources[0]['tag_list']

        list_command = ListArticlesCommand(token=authenticated_user['token'], tag='tag24')
        article_resources = ArticleService.list_articles(list_command)
        if len(article_resources) > 1:
            assert 'tag24' in article_resources[0]['tag_list']

    def test_listing_articles_with_author_filter(self, persisted_user, user1, user2, persisted_articles):
        # Authenticate user to generate valid token
        command = UserAuthenticationCommand(email='jake@jake.jake', password='nopass')
        authenticated_user = UserAuthenticationService.authenticate_user(command)

        list_command = ListArticlesCommand(token=authenticated_user['token'], author=user1.username)
        article_resources = ArticleService.list_articles(list_command)
        if len(article_resources) > 1:
            assert article_resources[0]['author']['username'] == user1.username
        no_of_user1_articles = len(article_resources)

        list_command = ListArticlesCommand(token=authenticated_user['token'], author=user2.username)
        article_resources = ArticleService.list_articles(list_command)
        if len(article_resources) > 1:
            assert article_resources[0]['author']['username'] == user2.username
        no_of_user2_articles = len(article_resources)

        assert no_of_user1_articles + no_of_user2_articles == 30

    def test_listing_articles_with_favorited_filter(self, persisted_user, user1, user2, persisted_articles):
        command = UserAuthenticationCommand(email=user1.email, password=user1.password)
        authenticated_user = UserAuthenticationService.authenticate_user(command)

        favorite_command = FavoriteArticleCommand(token=authenticated_user['token'], slug=persisted_articles[5].slug)
        UserFavoritingService.favorite_article(favorite_command)

        command = UserAuthenticationCommand(email='jake@jake.jake', password='nopass')
        authenticated_user = UserAuthenticationService.authenticate_user(command)

        list_command = ListArticlesCommand(token=authenticated_user['token'], favorited=user1.username)
        article_resources = ArticleService.list_articles(list_command)
        assert len(article_resources) == 1
        assert article_resources[0]['slug'] == persisted_articles[5].slug
