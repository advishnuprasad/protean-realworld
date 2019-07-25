from datetime import datetime

from protean.core.field.basic import DateTime, String

from realworld.domain import domain


@domain.aggregate
class Tag:
    name = String(required=True, max_length=50)
    added_at = DateTime(default=datetime.now())
    last_seen_at = DateTime(default=datetime.now())

    def touch(self):
        self.last_seen_at = datetime.now()

        return self
