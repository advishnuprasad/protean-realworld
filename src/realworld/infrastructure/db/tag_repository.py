from protean.core.exceptions import ObjectNotFoundError
from protean.globals import current_domain

from realworld.domain import domain
from realworld.model.tag import Tag


@domain.repository(aggregate_cls=Tag)
class TagRepository:
    def get_by_tag_name(self, tag_name):
        tag_dao = current_domain.get_dao(Tag)

        try:
            return tag_dao.find_by(name=tag_name.lower())
        except ObjectNotFoundError:
            return None

    def get_all(self):
        tag_dao = current_domain.get_dao(Tag)
        return tag_dao.query.limit(1000).all()
