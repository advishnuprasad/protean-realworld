import pytest

from realworld.application_services.command.get_comment_command import GetCommentCommand, GetAllCommentsCommand
from realworld.application_services.command.add_comment_command import AddCommentCommand
from realworld.application_services.command.delete_comment_command import DeleteCommentCommand
from realworld.application_services.command.user_authentication_command import UserAuthenticationCommand
from realworld.application_services.comment_service import CommentService
from realworld.application_services.user_authentication_service import UserAuthenticationService
from realworld.model.article import Article, Comment
from realworld.model.user import User


class TestCommentService:
    @pytest.fixture
    def persisted_user(self, test_domain):
        user_dao = test_domain.get_dao(User)
        user = user_dao.create(email='jake@jake.jake', username='jake', password='nopass')

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
    def persisted_comment(self, persisted_article, test_domain):
        comment_dao = test_domain.get_dao(Comment)
        comment = comment_dao.create(
            body='It takes a Jacobian',
            article=persisted_article,
            author=persisted_article.author)

        return comment

    def test_successful_get_article_comments(self, persisted_comment):
        auth_command = UserAuthenticationCommand(
            email=persisted_comment.author.email,
            password=persisted_comment.author.password)
        authenticated_user = UserAuthenticationService.authenticate_user(auth_command)

        comment_command = GetAllCommentsCommand(
            token=authenticated_user['token'],
            slug=persisted_comment.article.slug)
        comment_resources = CommentService.get_comments(comment_command)

        assert comment_resources is not None
        assert comment_resources[0]['body'] == 'It takes a Jacobian'

    def test_successful_get_comment(self, persisted_article):
        auth_command = UserAuthenticationCommand(
            email=persisted_article.author.email,
            password=persisted_article.author.password)
        authenticated_user = UserAuthenticationService.authenticate_user(auth_command)

        create_comment_command = AddCommentCommand(
            token=authenticated_user['token'],
            slug=persisted_article.slug,
            body='It takes a Jacobian')
        created_comment_resource = CommentService.add_comment(create_comment_command)

        comment_command = GetCommentCommand(slug=persisted_article.slug, identifier=created_comment_resource['id'])
        comment_resource = CommentService.get_comment(comment_command)

        assert comment_resource is not None
        assert comment_resource['body'] == 'It takes a Jacobian'

    def test_successful_add_comment(self, persisted_article):
        auth_command = UserAuthenticationCommand(
            email=persisted_article.author.email,
            password=persisted_article.author.password)
        authenticated_user = UserAuthenticationService.authenticate_user(auth_command)

        comment_command = AddCommentCommand(
            token=authenticated_user['token'],
            slug=persisted_article.slug,
            body='It takes a Jacobian')
        comment_resource = CommentService.add_comment(comment_command)

        assert comment_resource is not None
        assert comment_resource['body'] == 'It takes a Jacobian'

    def test_successful_delete_comment(self, persisted_article, test_domain):
        auth_command = UserAuthenticationCommand(
            email=persisted_article.author.email,
            password=persisted_article.author.password)
        authenticated_user = UserAuthenticationService.authenticate_user(auth_command)

        comment_command = AddCommentCommand(
            token=authenticated_user['token'],
            slug=persisted_article.slug,
            body='It takes a Jacobian')
        comment_resource = CommentService.add_comment(comment_command)

        assert comment_resource is not None
        assert comment_resource['body'] == 'It takes a Jacobian'

        # Now unfollow profile
        comment_command = DeleteCommentCommand(
            token=authenticated_user['token'],
            slug=persisted_article.slug,
            comment_identifier=comment_resource['id'])
        CommentService.delete_comment(comment_command)

        article_dao = test_domain.get_dao(Article)
        refreshed_article = article_dao.get(persisted_article.id)
        assert comment_resource['id'] not in [comment.identifier for comment in refreshed_article.comments]
