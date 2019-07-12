from datetime import datetime, timedelta

from protean.core.field.association import HasMany, Reference
from protean.core.field.basic import Boolean, DateTime, String

from realworld.domain import domain
from realworld.lib.jwt import generate_token


@domain.data_transfer_object
class UserRegistrationDTO:
    email = String(required=True, max_length=250)
    username = String(required=True, max_length=50)
    password = String(required=True, max_length=255)


@domain.aggregate
class User:
    email = String(required=True, max_length=250)
    username = String(required=True, max_length=50)
    password = String(required=True, max_length=255)
    bio = String(max_length=1024)
    token = String(max_length=1024)
    token_valid_until = DateTime()
    image = String(max_length=1024)

    follows = HasMany('realworld.model.user.Follower', via='user_id')
    followers = HasMany('realworld.model.user.Follower', via='following_id')

    @classmethod
    def register(self, user_dto: UserRegistrationDTO):
        return User(email=user_dto.email, username=user_dto.username, password=user_dto.password)

    def authenticate(self, password: str):
        return password == self.password

    def refresh_token(self):
        token = generate_token(self.id)

        self.token = token
        self.token_valid_until = datetime.now() + timedelta(days=1)

    def update(self, **kwargs):
        valid_fields = [
            field for field in kwargs
            if field in ['email', 'username', 'password', 'image', 'bio']]

        for field in valid_fields:
            setattr(self, field, kwargs[field])

    ####################
    # Follower methods #
    ####################
    def follow(self, user: 'User'):
        if user not in [follow_object.following for follow_object in self.follows]:
            self.follows.add(Follower(following=user, user=self))

        return self

    def unfollow(self, user: 'User'):
        [follow_object] = [
            follow_object for follow_object
            in self.follows
            if follow_object.following == user]

        self.follows.remove(follow_object)

        return self


@domain.entity(aggregate_cls=User)
class Follower:
    following = Reference(User, required=True)
    user = Reference(User, required=True)
    followed_on = DateTime(required=True, default=datetime.now())


@domain.data_transfer_object
class ProfileDTO:
    username = String(required=True, max_length=50)
    bio = String(max_length=1024)
    image = String(max_length=1024)
    following = Boolean(default=False)

    @classmethod
    def for_user(cls, user: User, profile_user: User):
        following = profile_user in [item.following for item in user.follows]

        return ProfileDTO(
            username=profile_user.username,
            bio=profile_user.bio,
            image=profile_user.image,
            following=following
        )
