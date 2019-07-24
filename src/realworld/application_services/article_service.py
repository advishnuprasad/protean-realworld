from protean.globals import current_domain

from realworld.application_services.command.create_article_command import CreateArticleCommand
from realworld.application_services.command.delete_article_command import DeleteArticleCommand
from realworld.application_services.command.get_article_command import GetArticleCommand
from realworld.application_services.command.list_articles_command import ListArticlesCommand
from realworld.application_services.command.update_article_command import UpdateArticleCommand
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

    @classmethod
    def list_articles(cls, command: ListArticlesCommand):
        article_repo = current_domain.repository_for(Article)

        articles = None
        if command.tag is not None:
            articles = article_repo.get_by_tag(command.tag, command.limit, command.offset)
        elif command.author is not None:
            articles = article_repo.get_by_author(command.author, command.limit, command.offset)
        elif command.favorited is not None:
            articles = article_repo.get_by_favorited(command.favorited, command.limit, command.offset)
        else:
            articles = article_repo.list_articles(command.limit, command.offset)

        if articles is not None:
            article_resource = ArticleRepresentation().dump(articles, many=True)
            return article_resource

        return None

    @classmethod
    def update_article(cls, command: UpdateArticleCommand):
        user_repo = current_domain.repository_for(User)
        user = user_repo.get_by_token(command.token)

        if user is not None:
            article_repo = current_domain.repository_for(Article)
            article = article_repo.get_by_slug(command.slug)

            if article is not None:
                kwargs = command.to_dict()
                kwargs.pop('token', None)
                kwargs = {k: v for k, v in kwargs.items() if v is not None}
                article.update(**kwargs)
                article_repo.add(article)

                article_resource = ArticleRepresentation().dump(article)
                return article_resource

        return None

    @classmethod
    def delete_article(cls, command: DeleteArticleCommand):
        user_repo = current_domain.repository_for(User)
        user = user_repo.get_by_token(command.token)

        if user is not None:
            article_repo = current_domain.repository_for(Article)
            article = article_repo.get_by_slug(command.slug)

            if article is not None:
                article_repo.remove(article)

        return None
