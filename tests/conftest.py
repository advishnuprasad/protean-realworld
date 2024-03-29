import os
import pytest


@pytest.fixture(autouse=True)
def test_domain():
    from realworld.domain import domain

    # Construct relative path to config file
    current_path = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(current_path, "./config.py")

    if os.path.exists(config_path):
        domain.config.from_pyfile(config_path)

    with domain.domain_context():
        yield domain


@pytest.fixture(autouse=True)
def run_around_tests(test_domain):

    yield

    if test_domain.has_provider('default'):
        test_domain.get_provider('default')._data_reset()
