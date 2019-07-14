from protean.core.field.basic import Identifier, String

from realworld.domain import domain


@domain.data_transfer_object
class DeleteCommentCommand:
    token = String(max_length=1024)
    slug = String(required=True, max_length=250)
    comment_identifier = Identifier()
