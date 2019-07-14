from protean.core.field.basic import String, Text

from realworld.domain import domain


@domain.data_transfer_object
class AddCommentCommand:
    token = String(max_length=1024)
    slug = String(required=True, max_length=250)
    body = Text(required=True)
