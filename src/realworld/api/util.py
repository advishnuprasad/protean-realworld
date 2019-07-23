import json

from collections import defaultdict

from protean.globals import current_domain

from realworld.model.article import Article
from realworld.model.user import User


def load_data(json_file):
    user_dao = current_domain.get_dao(User)
    article_dao = current_domain.get_dao(Article)

    try:
        with open(json_file) as f:
            data = json.load(f)

            counts = defaultdict(int)
            for entity in data:
                if entity == 'user':
                    for item in data[entity]:
                        user_dao.create(**item)
                        counts['user'] += 1
                elif entity == 'article':
                    for item in data[entity]:
                        article_dao.create(**item)
                        counts['article'] += 1

            print('Counts: {}'.format(dict(counts)))
    except (OSError, FileNotFoundError) as e:
        print("ERROR LOADING DATA FILE:", json_file, " because: ", e)
