from realworld.domain import domain
from realworld.application_services.command.new_tags_command import NewTagsCommand
from realworld.application_services.tag_service import TagService
from realworld.model.article import TagsAdded
from realworld.model.tag import Tag


@domain.subscriber(aggregate_cls=Tag, domain_event=TagsAdded)
class UpsertTags:
    """Subscriber that stores Tags encountered in Articles
    """

    def notify(self, domain_event):
        command = NewTagsCommand(tag_list=domain_event.tag_list, added_at=domain_event.added_at)
        TagService.add_tags(command)
