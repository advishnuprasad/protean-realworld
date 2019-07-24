import os

from flask import Flask

from realworld.api.views.user import user_api
from realworld.api.views.profile import profile_api
from realworld.api.views.article import article_api
from realworld.api.views.comment import comment_api
from realworld.api.views.favorite import favorite_api
from realworld.domain import domain

from realworld.api.util import load_data

app = Flask(__name__, static_folder=None)
app.register_blueprint(user_api)
app.register_blueprint(profile_api)
app.register_blueprint(article_api)
app.register_blueprint(comment_api)
app.register_blueprint(favorite_api)

# Configure domain
current_path = os.path.abspath(os.path.dirname(__file__))
config_path = os.path.join(current_path, "./../config.py")
domain.config.from_pyfile(config_path)

# Push up a Domain Context
# This should be done within Flask App
context = domain.domain_context()
context.push()


@app.before_first_request
def before_first_request():
    data_file = os.environ.get('DATA')
    if data_file:
        load_data(data_file)
