from datetime import datetime

from protean.core.field.basic import Boolean, CustomObject, DateTime, Integer, List, String, Text
from protean.core.field.association import Reference

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


@domain.aggregate
class Article:
    slug = String(max_length=250)
    title = String(required=True, max_length=250)
    description = Text(required=True)
    body = Text(required=True)
    tag_list = List()
    created_at = DateTime(default=datetime.now())
    updated_at = DateTime(default=datetime.now())
    favorited = Boolean(default=False)
    favorites_count = Integer()

    author = Reference(User, required=True)

    @classmethod
    def create(self, article_dto: CreateArticleDTO):
        return Article(
            title=article_dto.title,
            slug=slugify(article_dto.title),
            description=article_dto.description,
            body=article_dto.body,
            tag_list=article_dto.tag_list,
            author=article_dto.author
            )

    def update(self, **kwargs):
        valid_fields = [
            field for field in kwargs
            if field in ['title', 'description', 'body']]

        for field in valid_fields:
            setattr(self, field, kwargs[field])

        if 'title' in valid_fields:
            setattr(self, 'slug', slugify(self.title))
