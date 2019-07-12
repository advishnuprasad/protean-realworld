import pytest

from uuid import UUID

from protean.core.exceptions import ValidationError

from realworld.model.article import Article, CreateArticleDTO
from realworld.model.user import User


class TestUser:
    def test_that_an_article_can_be_initialized_successfully(self):
        article = Article(
            title="How to train your dragon",
            description="Ever wonder how?",
            body="You have to believe",
            tagList=["reactjs", "angularjs", "dragons"]
        )
        assert article is not None

    def test_that_mandatory_fields_are_validated(self):
        with pytest.raises(ValidationError):
            Article()

    def test_that_a_new_article_can_be_created_successfully(self):
        user = User(email='jake@jake.jake', username='jake', password='nopass')

        article_dto = CreateArticleDTO(
            title="How to train your dragon",
            description="Ever wonder how?",
            body="You have to believe",
            tag_list=["reactjs", "angularjs", "dragons"],
            author=user
        )

        article = Article.create(article_dto)

        assert article is not None
        assert isinstance(article, Article)
        assert article.id is not None

        try:
            UUID(str(article.id))
        except ValueError:
            pytest.fail("ID is not valid UUID")

    def test_that_a_slug_is_created_from_the_article_title(self):
        user = User(email='jake@jake.jake', username='jake', password='nopass')

        article_dto = CreateArticleDTO(
            title="How to train your dragon",
            description="Ever wonder how?",
            body="You have to believe",
            tag_list=["reactjs", "angularjs", "dragons"],
            author=user
        )

        article = Article.create(article_dto)

        assert article.slug is not None
        assert article.slug == "how-to-train-your-dragon"
