from protean.core.exceptions import ObjectNotFoundError
from protean.globals import current_domain

from realworld.domain import domain
from realworld.model.article import Article
from realworld.model.user import User


@domain.repository(aggregate_cls=Article)
class ArticleRepository:
    def get_by_slug(self, slug: str) -> Article:
        article_dao = current_domain.get_dao(Article)
        try:
            return article_dao.find_by(slug=slug)
        except ObjectNotFoundError:
            return None

    def get_by_tag(self, tag: str, limit: int, offset: int):
        article_dao = current_domain.get_dao(Article)
        return article_dao.query.filter(tag_list__contains=tag).limit(limit).offset(offset).all()

    def get_by_author(self, author: str, limit: int, offset: int):
        user_repo = current_domain.repository_for(User)
        article_dao = current_domain.get_dao(Article)
        user = user_repo.get_by_username(author)
        if user is not None:
            return article_dao.query.filter(author_id=user.id).limit(limit).offset(offset).all()

        return None

    def get_by_favorited(self, favorited: str, limit: int, offset: int):
        user_repo = current_domain.repository_for(User)
        user = user_repo.get_by_username(favorited)
        if user is not None:
            return [favorite.article for favorite in user.favorites]

        return None

    def list_articles(self, limit: int, offset: int):
        article_dao = current_domain.get_dao(Article)
        return article_dao.query.limit(limit).offset(offset).all()
