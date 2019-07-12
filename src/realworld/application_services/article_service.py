from protean.globals import current_domain

from realworld.application_services.command.create_article_command import CreateArticleCommand
from realworld.application_services.command.get_article_command import GetArticleCommand
from realworld.application_services.representation.article_representation import ArticleRepresentation
from realworld.infrastructure.article_repository import ArticleRepository  # noqa: F401  # FIXME No need to import
from realworld.model.article import Article, CreateArticleDTO
from realworld.model.user import User
from realworld.domain import domain


@domain.application_service
class ArticleService:
    @classmethod
    def create_article(cls, command: CreateArticleCommand):
        user_repo = current_domain.repository_for(User)
        user = user_repo.get_by_token(command.token)

        if user is not None:
            # Convert a Command Object into a DTO, to pass into the domain
            article_dto = CreateArticleDTO(
                title=command.title,
                description=command.description,
                body=command.body,
                tag_list=command.tag_list,
                author=user
            )

            # Call a factory method to construct a Articl object
            article = Article.create(article_dto)

            # Persist the new Article object
            article_repo = current_domain.repository_for(Article)
            article_repo.add(article)

            # Convert the persisted article object into a resource
            #   to be passed onto the callee
            article_resource = ArticleRepresentation().dump(article)
            return article_resource

        return None

    @classmethod
    def get_article(cls, command: GetArticleCommand):
        article_repo = current_domain.repository_for(Article)
        article = article_repo.get_by_slug(command.slug)

        if article is not None:
            article_resource = ArticleRepresentation().dump(article)
            return article_resource

        return None
