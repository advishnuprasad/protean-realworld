from protean.core.field.basic import DateTime, Identifier, Nested, Text

from realworld.domain import domain
from realworld.application_services.representation.user_representation import UserRepresentation
from realworld.model.article import Article


@domain.serializer(aggregate_cls=Article)
class CommentRepresentation:
    id = Identifier()
    body = Text(required=True)
    created_at = DateTime()
    updated_at = DateTime()

    author = Nested(UserRepresentation, required=True)
