from protean.core.exceptions import ObjectNotFoundError
from protean.globals import current_domain

from realworld.domain import domain
from realworld.model.article import Article


@domain.repository(aggregate_cls=Article)
class ArticleRepository:
    @classmethod
    def get_by_slug(cls, slug: str) -> Article:
        article_dao = current_domain.get_dao(Article)
        try:
            return article_dao.find_by(slug=slug)
        except ObjectNotFoundError:
            return None
