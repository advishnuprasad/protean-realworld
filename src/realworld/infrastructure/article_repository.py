from realworld.domain import domain
from realworld.model.article import Article


@domain.repository(aggregate_cls=Article)
class ArticleRepository:
    pass
