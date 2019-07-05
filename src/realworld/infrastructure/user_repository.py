from protean.globals import current_domain

from realworld.domain import domain
from realworld.model.user import User


@domain.repository(aggregate_cls=User)
class UserRepository:
    @classmethod
    def get_by_email(cls, email: str) -> User:
        user_dao = current_domain.get_dao(User)
        return user_dao.find_by(email=email)
