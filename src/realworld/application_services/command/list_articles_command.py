from protean.core.field.basic import Integer, String


from realworld.domain import domain


@domain.data_transfer_object
class ListArticlesCommand:
    token = String(max_length=1024)
    tag = String(max_length=50)
    author = String(max_length=50)
    favorited = String(max_length=50)
    limit = Integer(default=20)
    offset = Integer(default=0)
