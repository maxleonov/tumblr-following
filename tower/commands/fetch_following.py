import logging

import click
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from tower.database import Session
from tower.model import Following
from tower.tumblr_client import get_tumblr_client

l = logging.getLogger(__name__)


@click.command('fetch-following')
@click.option('--delete-first', is_flag=True, default=False, help='Delete values from the DB before fetching')
def fetch_following(delete_first: bool):
    tumblr_client = get_tumblr_client()

    user_info = tumblr_client.info()
    user_name = user_info['user']['name']

    session = Session()

    if delete_first:
        session.query(Following).filter(
            Following.user_name == user_name
        ).delete()

    offset = 0

    while True:
        l.info('Fetching blogs followed by "%s" starting at %s', user_name, offset)

        response = tumblr_client.following(
            offset=offset
        )

        try:
            assert(len(response['blogs']))
        except AssertionError:
            l.info('All items have been fetched!')
            break

        counter = 0

        for blog in response['blogs']:
            session.add(Following(
                user_name=user_name,
                blog_name=blog['name'],
                title=blog['title'],
                description=blog['description'],
                url=blog['url']
            ))

            try:
                session.commit()
            except (IntegrityError, InvalidRequestError):
                session.rollback()
                pass
            else:
                counter += 1

        l.info('%s items saved', counter)

        offset += len(response['blogs'])
