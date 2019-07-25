from datetime import datetime

from protean.core.field.basic import DateTime, List

from realworld.domain import domain


@domain.data_transfer_object
class NewTagsCommand:
    tag_list = List()
    added_at = DateTime(default=datetime.now())
