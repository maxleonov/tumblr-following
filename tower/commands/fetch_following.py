import logging

import click

from tower.database import Session
from tower.model import Following
from tower.tumblr_client import get_tumblr_client

l = logging.getLogger(__name__)


@click.command('fetch-following')
def fetch_following():
    tumblr_client = get_tumblr_client()

    user_info = tumblr_client.info()
    user_name = user_info['user']['name']

    session = Session()

    while True:
        offset = session.query(Following).count()

        l.info('Fetching blogs followed by "%s" starting at %s', user_name, offset)

        response = tumblr_client.following(
            offset=offset
        )

        try:
            assert(len(response['blogs']))
        except AssertionError:
            l.info('All items have been fetched!')
            break

        for blog in response['blogs']:
            session.add(Following(
                name=blog['name'],
                title=blog['title'],
                description=blog['description'],
                url=blog['url']
            ))

        session.commit()
