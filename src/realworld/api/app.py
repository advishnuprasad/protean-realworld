import os

from flask import Flask, render_template, url_for

from realworld.api.views.user import user_api
from realworld.domain import domain

app = Flask(__name__)
app.register_blueprint(user_api)

# Configure domain
current_path = os.path.abspath(os.path.dirname(__file__))
config_path = os.path.join(current_path, "./../config.py")
domain.config.from_pyfile(config_path)

# Push up a Domain Context
# This should be done within Flask App
context = domain.domain_context()
context.push()


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route('/')
def routes():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return render_template("home.html", links=links)
