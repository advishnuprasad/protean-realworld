import pytest

from datetime import datetime, timedelta

from realworld.application_services.command.new_tags_command import NewTagsCommand
from realworld.application_services.tag_service import TagService
from realworld.model.tag import Tag


class TestArticleService:

    @pytest.fixture
    def persisted_tags(self, test_domain):
        tag_dao = test_domain.get_dao(Tag)
        tags_list = ["tag{}".format(i) for i in range(1, 25)]

        tags = []
        for tag in tags_list:
            tags.append(tag_dao.create(name=tag, added_at=datetime.now(), last_seen_at=datetime.now()))

        return tags

    def test_successful_addition_of_tags(self, test_domain):
        command = NewTagsCommand(tag_list=['tag1', 'tag2'])
        TagService.add_tags(command)

        # FIXME Should check for this via Repository itself
        tag_dao = test_domain.get_dao(Tag)
        persisted_tags = tag_dao.query.all()
        assert len(persisted_tags.items) == 2

    def test_successful_update_of_tags(self, test_domain):
        # FIXME Should check for this via Repository itself
        tag_dao = test_domain.get_dao(Tag)

        command1 = NewTagsCommand(tag_list=['tag1', 'tag2'], added_at=datetime.now() - timedelta(minutes=5))
        TagService.add_tags(command1)

        persisted_tags = tag_dao.query.all()
        assert len(persisted_tags.items) == 2

    def test_successful_upsert_of_tag_lists(self, test_domain):
        # FIXME Should check for this via Repository itself
        tag_dao = test_domain.get_dao(Tag)

        command1 = NewTagsCommand(tag_list=['tag1', 'tag2'], added_at=datetime.now() - timedelta(minutes=5))
        TagService.add_tags(command1)

        persisted_tags = tag_dao.query.all()
        assert len(persisted_tags.items) == 2

        command2 = NewTagsCommand(tag_list=['tag3', 'tag4', 'tag1'], added_at=datetime.now() - timedelta(minutes=5))
        TagService.add_tags(command2)

        persisted_tags = tag_dao.query.all()
        assert len(persisted_tags.items) == 4

    def test_successful_update_of_tag_timestamps(self, test_domain):
        # FIXME Should check for this via Repository itself
        tag_dao = test_domain.get_dao(Tag)

        command1 = NewTagsCommand(tag_list=['tag1', 'tag2'], added_at=datetime.now() - timedelta(minutes=5))
        TagService.add_tags(command1)

        persisted_tags = tag_dao.query.all()
        assert len(persisted_tags.items) == 2
        ts_added_at = persisted_tags.items[0].added_at
        ts_last_seen_at = persisted_tags.items[0].last_seen_at

        command2 = NewTagsCommand(tag_list=['tag1', 'tag2'])
        TagService.add_tags(command2)

        # FIXME Should check for this via Repository itself
        persisted_tags = tag_dao.query.all()
        assert len(persisted_tags.items) == 2
        assert persisted_tags.items[0].added_at == ts_added_at
        assert persisted_tags.items[0].last_seen_at > ts_last_seen_at

    def test_successful_tags_retrieval(self, test_domain, persisted_tags):
        tags_resource = TagService.get_tags()

        assert tags_resource is not None
        assert len(tags_resource['tags']) == 24
