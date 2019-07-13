from protean.core.field.basic import String, Text

from realworld.domain import domain


@domain.data_transfer_object
class UpdateArticleCommand:
    token = String(required=True, max_length=1024)
    slug = String(required=True, max_length=250)
    title = String(max_length=250)
    description = Text()
    body = Text()
