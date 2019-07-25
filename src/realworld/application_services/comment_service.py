from protean.globals import current_domain

from realworld.application_services.command.add_comment_command import AddCommentCommand
from realworld.application_services.command.get_comment_command import GetCommentCommand, GetAllCommentsCommand
from realworld.application_services.command.delete_comment_command import DeleteCommentCommand
from realworld.application_services.representation.comment_representation import CommentRepresentation
from realworld.domain import domain
from realworld.infrastructure.db.article_repository import ArticleRepository  # noqa: F401  # FIXME No need to import
from realworld.model.article import Article
from realworld.model.user import User


@domain.application_service
class CommentService:
    @classmethod
    def get_comment(cls, command: GetCommentCommand):
        article_repo = current_domain.repository_for(Article)
        article = article_repo.get_by_slug(command.slug)

        if article is not None:
            comment = article.get_comment_by_identifier(command.identifier)
            comment_resource = CommentRepresentation().dump(comment)

            return comment_resource

        return None

    @classmethod
    def get_comments(cls, command: GetAllCommentsCommand):
        user_repo = current_domain.repository_for(User)
        logged_in_user = user_repo.get_by_token(command.token)

        if logged_in_user is not None:
            article_repo = current_domain.repository_for(Article)
            article = article_repo.get_by_slug(command.slug)

            if article is not None:
                comment_resource = CommentRepresentation().dump(article.comments, many=True)
                return comment_resource

        return None

    @classmethod
    def add_comment(cls, command: AddCommentCommand):
        user_repo = current_domain.repository_for(User)
        logged_in_user = user_repo.get_by_token(command.token)

        if logged_in_user is not None:
            article_repo = current_domain.repository_for(Article)
            article = article_repo.get_by_slug(command.slug)

            if article is not None:
                updated_article, new_comment = article.add_comment(command.body, logged_in_user)
                article_repo.add(updated_article)

                fetch_command = GetCommentCommand(slug=article.slug, identifier=new_comment.id)
                return cls.get_comment(fetch_command)

        return None

    @classmethod
    def delete_comment(cls, command: DeleteCommentCommand):
        user_repo = current_domain.repository_for(User)
        logged_in_user = user_repo.get_by_token(command.token)

        if logged_in_user is not None:
            article_repo = current_domain.repository_for(Article)
            article = article_repo.get_by_slug(command.slug)

            if article is not None:
                article.delete_comment(command.comment_identifier)
                article_repo.add(article)

        return None
