from protean.core.field.basic import String

from realworld.domain import domain


@domain.data_transfer_object
class UnfavoriteArticleCommand:
    token = String(required=True, max_length=1024)
    slug = String(required=True, max_length=250)
