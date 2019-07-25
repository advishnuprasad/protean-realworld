from protean.globals import current_domain

from realworld.application_services.command.new_tags_command import NewTagsCommand
from realworld.application_services.representation.tags_representation import TagsRepresentation
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

    @classmethod
    def get_tags(cls):
        tag_repo = current_domain.repository_for(Tag)
        tags = tag_repo.get_all()

        if tags is not None:
            tags_list = [tag.name for tag in tags]
            tags_resource = TagsRepresentation().dump(tags_list)
            return tags_resource

        return None
