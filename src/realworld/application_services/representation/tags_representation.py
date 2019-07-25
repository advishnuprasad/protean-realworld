from realworld.domain import domain
from realworld.model.tag import Tag


@domain.serializer(aggregate_cls=Tag)
class TagsRepresentation:
    def dump(self, tags):
        return {
            "tags": tags
        }
