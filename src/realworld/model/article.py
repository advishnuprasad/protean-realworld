from datetime import datetime

from protean.core.field.basic import Boolean, CustomObject, DateTime, Integer, List, String, Text
from protean.core.field.association import HasMany, Reference
from protean.globals import current_domain

from realworld.domain import domain
from realworld.lib.utils import slugify
from realworld.model.user import User


@domain.data_transfer_object
class CreateArticleDTO:
    title = String(required=True, max_length=250)
    description = Text(required=True)
    body = Text(required=True)
    tag_list = List()

    author = CustomObject(User, required=True)


@domain.domain_event
class TagsAdded:
    tag_list = List()
    added_at = DateTime(default=datetime.now())


@domain.aggregate
class Article:
    slug = String(max_length=250)
    title = String(required=True, max_length=250)
    description = Text(required=True)
    body = Text(required=True)
    tag_list = List()
    created_at = DateTime(default=datetime.now())
    updated_at = DateTime(default=datetime.now())

    author = Reference(User, required=True)

    comments = HasMany('realworld.model.article.Comment')

    @classmethod
    def create(self, article_dto: CreateArticleDTO):
        article = Article(
            title=article_dto.title,
            slug=slugify(article_dto.title),
            description=article_dto.description,
            body=article_dto.body,
            tag_list=article_dto.tag_list,
            author=article_dto.author
            )

        current_domain.publish(TagsAdded(tag_list=article_dto.tag_list))

        return article

    def update(self, **kwargs):
        valid_fields = [
            field for field in kwargs
            if field in ['title', 'description', 'body']]

        for field in valid_fields:
            setattr(self, field, kwargs[field])

        if 'title' in valid_fields:
            setattr(self, 'slug', slugify(self.title))

    ###################
    # Comment methods #
    ###################
    def add_comment(self, body: String, logged_in_user: User):
        new_comment = Comment(body=body, article=self, author=logged_in_user)
        self.comments.add(new_comment)

        return self, new_comment

    def delete_comment(self, comment_identifier):
        [old_comment] = [
            comment for comment
            in self.comments
            if comment.id == comment_identifier]

        self.comments.remove(old_comment)

        return self, old_comment

    def get_comment_by_identifier(self, comment_identifier):
        [comment] = [
            comment for comment
            in self.comments
            if comment.id == comment_identifier]

        return comment


@domain.data_transfer_object(aggregate_cls=Article)
class ArticleDTO:
    slug = String(max_length=250)
    title = String(required=True, max_length=250)
    description = Text(required=True)
    body = Text(required=True)
    tag_list = List()
    created_at = DateTime(default=datetime.now())
    updated_at = DateTime(default=datetime.now())
    favorited = Boolean(default=False)
    favorites_count = Integer()

    @classmethod
    def for_article(cls, article: Article, user: User):
        favorited = article in [favorite.article for favorite in user.favorites]

        return ArticleDTO(
            slug=article.slug,
            title=article.title,
            description=article.description,
            body=article.body,
            tag_list=article.tag_list,
            created_at=article.created_at,
            updated_at=article.updated_at,
            author=article.author,
            favorited=favorited
        )


@domain.entity(aggregate_cls=Article)
class Comment:
    body = Text(required=True)
    created_at = DateTime(default=datetime.now())
    updated_at = DateTime(default=datetime.now())

    article = Reference(Article, required=True)
    author = Reference(User, required=True)
