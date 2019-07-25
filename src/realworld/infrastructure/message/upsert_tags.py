from realworld.domain import domain
from realworld.model.article import TagsAdded
from realworld.model.tag import Tag


@domain.subscriber(aggregate_cls=Tag, domain_event=TagsAdded)
class UpsertTags:
    """Subscriber that stores Tags encountered in Articles
    """

    def notify(self, domain_event):
        print("1---> Received Domain Event: ", domain_event)
