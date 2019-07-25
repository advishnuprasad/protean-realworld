from realworld.model.tag import Tag


class TestTag:

    def test_that_a_tag_can_be_initialized_successfully(self):
        tag = Tag(name='test-tag')

        assert tag is not None
        assert tag.added_at is not None
        assert tag.last_seen_at is not None

    def test_that_a_tag_can_be_touched_and_updated(self):
        tag = Tag(name='test-tag')

        tag.touch()
        assert tag.last_seen_at != tag.added_at
        assert tag.last_seen_at > tag.added_at
