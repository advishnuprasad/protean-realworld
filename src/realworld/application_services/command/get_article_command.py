from protean.core.field.basic import String

from realworld.domain import domain


@domain.data_transfer_object
class GetArticleCommand:
    token = String(max_length=1024)
    slug = String(max_length=250)
