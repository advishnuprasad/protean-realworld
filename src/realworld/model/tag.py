from datetime import datetime

from protean.core.field.basic import DateTime, String

from realworld.domain import domain


@domain.aggregate
class Tag:
    name = String(required=True, max_length=50)
    added_at = DateTime(default=datetime.now())
    last_seen_at = DateTime(default=datetime.now())

    @classmethod
    def create(self, tag_name, added_at=datetime.now()):
        return Tag(name=tag_name.lower(), added_at=added_at, last_seen_at=added_at)

    def touch(self, updated_at=datetime.now()):
        self.last_seen_at = updated_at

        return self
