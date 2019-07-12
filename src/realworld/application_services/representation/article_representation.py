from protean.core.field.basic import Identifier, List, Nested, String, Text

from realworld.domain import domain
from realworld.application_services.representation.profile_representation import ProfileRepresentation
from realworld.model.article import Article


@domain.serializer(aggregate_cls=Article)
class ArticleRepresentation:
    id = Identifier()
    title = String(required=True, max_length=250)
    description = Text(required=True)
    body = Text(required=True)
    tag_list = List()

    author = Nested(ProfileRepresentation, required=True)
