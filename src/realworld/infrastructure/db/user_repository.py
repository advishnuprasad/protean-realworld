from protean.core.exceptions import ObjectNotFoundError
from protean.globals import current_domain

from realworld.domain import domain
from realworld.model.user import User


@domain.repository(aggregate_cls=User)
class UserRepository:
    @classmethod
    def get_by_email(cls, email: str) -> User:
        user_dao = current_domain.get_dao(User)
        try:
            return user_dao.find_by(email=email)
        except ObjectNotFoundError:
            return None

    @classmethod
    def get_by_username(cls, username: str) -> User:
        user_dao = current_domain.get_dao(User)
        try:
            return user_dao.find_by(username=username)
        except ObjectNotFoundError:
            return None

    @classmethod
    def get_by_token(cls, token: str) -> User:
        # FIXME Should return None if token has expired
        user_dao = current_domain.get_dao(User)
        try:
            user = user_dao.find_by(token=token)
            return user
        except ObjectNotFoundError:
            return None
