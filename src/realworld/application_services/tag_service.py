from protean.globals import current_domain

from realworld.application_services.command.new_tags_command import NewTagsCommand
from realworld.domain import domain
from realworld.infrastructure.db.tag_repository import TagRepository  # noqa: F401  # FIXME No need to import
from realworld.model.tag import Tag


@domain.application_service
class TagService:
    @classmethod
    def add_tags(cls, command: NewTagsCommand):
        tag_repo = current_domain.repository_for(Tag)

        for tag_name in command.tag_list:
            tag = tag_repo.get_by_tag_name(tag_name)

            if tag:
                tag.touch(command.added_at)
            else:
                tag = Tag.create(tag_name, command.added_at)

            tag_repo.add(tag)
