from protean.core.field.basic import Identifier, String

from realworld.domain import domain


@domain.data_transfer_object
class GetCommentCommand:
    slug = String(required=True, max_length=250)
    identifier = Identifier(required=True)


@domain.data_transfer_object
class GetAllCommentsCommand:
    token = String(max_length=1024)
    slug = String(max_length=250)
