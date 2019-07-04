from realworld.domain import domain
from realworld.model.user import User


@domain.repository(aggregate_cls=User)
class UserRepository:
    """User Repository class"""
    # FIXME Can we avoid declaring this repository explicitly?
