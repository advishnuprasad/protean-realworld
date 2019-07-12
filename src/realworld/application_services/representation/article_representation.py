from protean.core.field.basic import CustomObject, Identifier, List, String, Text

from realworld.domain import domain
from realworld.model.article import Article
from realworld.model.user import User


@domain.data_transfer_object
class ArticleRepresentation:
    id = Identifier()
    title = String(required=True, max_length=250)
    description = Text(required=True)
    body = Text(required=True)
    tag_list = List()

    author = CustomObject(User, required=True)

    @classmethod
    def from_article(cls, article: Article):
        return ArticleRepresentation(
            id=article.id,
            title=article.title,
            description=article.description,
            body=article.body,
            tag_list=article.tag_list,
            author=article.author
        )
