from protean.core.field.basic import String

from realworld.domain import domain


@domain.data_transfer_object
class CurrentUserCommand:
    token = String(required=True, max_length=255)
