from protean.core.field.basic import List, String, Text

from realworld.domain import domain


@domain.data_transfer_object
class CreateArticleCommand:
    token = String(required=True, max_length=1024)
    title = String(required=True, max_length=250)
    description = Text(required=True)
    body = Text(required=True)
    tag_list = List()
