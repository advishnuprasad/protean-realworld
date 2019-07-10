from protean.core.field.basic import String

from realworld.domain import domain


@domain.data_transfer_object
class FetchProfileCommand:
    token = String(max_length=1024)
    username = String(required=True, max_length=50)
