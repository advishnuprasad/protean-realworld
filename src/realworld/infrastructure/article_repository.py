from protean.core.exceptions import ObjectNotFoundError
from protean.globals import current_domain

from realworld.domain import domain
from realworld.model.article import Article


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
        return article_dao.query.filter(tag_list__contains=tag).all()

    def get_by_author(self, author: str, limit: int, offset: int):
        article_dao = current_domain.get_dao(Article)
        return article_dao.query.filter(author=author).all()

    def get_by_favorited(self, favorited: str, limit: int, offset: int):
        article_dao = current_domain.get_dao(Article)
        return article_dao.query.filter(favorited=favorited).all()

    def list_articles(self, limit: int, offset: int):
        article_dao = current_domain.get_dao(Article)
        return article_dao.query.limit(limit).offset(offset).all()
