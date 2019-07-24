from protean.globals import current_domain

from realworld.application_services.command.favorite_article_command import FavoriteArticleCommand
from realworld.application_services.command.unfavorite_article_command import UnfavoriteArticleCommand
from realworld.application_services.representation.article_representation import ArticleRepresentation
from realworld.infrastructure.user_repository import UserRepository  # noqa: F401  # FIXME No need to import
from realworld.infrastructure.article_repository import ArticleRepository  # noqa: F401  # FIXME No need to import
from realworld.model.article import Article, ArticleDTO
from realworld.model.user import User
from realworld.domain import domain


@domain.application_service
class UserFavoritingService:
    @classmethod
    def favorite_article(cls, command: FavoriteArticleCommand):
        user_repo = current_domain.repository_for(User)
        user = user_repo.get_by_token(command.token)

        if user is not None:
            article_repo = current_domain.repository_for(Article)
            article = article_repo.get_by_slug(command.slug)

            if article is not None:
                user.favorite(article)
                user_repo.add(user)

                updated_user = user_repo.get(user.id)  # FIXME Do we need to refresh the underlying object always?
                article_dto = ArticleDTO.for_article(article, updated_user)
                article_resource = ArticleRepresentation().dump(article_dto)
                return article_resource

        return None

    @classmethod
    def unfavorite_article(cls, command: UnfavoriteArticleCommand):
        user_repo = current_domain.repository_for(User)
        user = user_repo.get_by_token(command.token)

        if user is not None:
            article_repo = current_domain.repository_for(Article)
            article = article_repo.get_by_slug(command.slug)

            if article is not None:
                user.unfavorite(article)
                user_repo.add(user)

                updated_user = user_repo.get(user.id)  # FIXME Do we need to refresh the underlying object always?
                article_dto = ArticleDTO.for_article(article, updated_user)
                article_resource = ArticleRepresentation().dump(article_dto)
                return article_resource

        return None
