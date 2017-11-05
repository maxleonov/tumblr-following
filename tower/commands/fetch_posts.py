import datetime
import logging

import click
from sqlalchemy.exc import IntegrityError

from tower.database import Session
from tower.model import Post
from tower.tumblr_client import get_tumblr_client
from tower.commands import HELP_FETCH_POSTS_NEWER_FIRST

l = logging.getLogger(__name__)


@click.command('fetch-posts')
@click.argument('blog-name')
@click.option('--newer-first', is_flag=True, default=False, help=HELP_FETCH_POSTS_NEWER_FIRST)
def fetch_posts(blog_name: str, newer_first: bool):
    tumblr_client = get_tumblr_client()
    session = Session()

    offset = 0

    while True:
        if not newer_first:
            offset = session.query(Post).filter(Post.blog_name == blog_name).count()

        l.info('Fetching "%s" posts starting at %s', blog_name, offset)

        response = tumblr_client.posts(
            '{}.tumblr.com'.format(blog_name),
            reblog_info=True,
            offset=offset
        )

        try:
            assert(len(response['posts']))
        except AssertionError:
            l.info('All items have been fetched!')
            return
        else:
            if newer_first:
                offset += len(response['posts'])

        for post in response['posts']:
            session.add(Post(
                id=post['id'],
                post_url=post['post_url'],
                blog_name=response['blog']['name'],
                type=post['type'],
                reblogged_from_name=post.get('reblogged_from_name'),
                reblogged_root_name=post.get('reblogged_root_name'),
                date=datetime.datetime.strptime(post['date'], '%Y-%m-%d %H:%M:%S GMT')
            ))

            try:
                session.commit()
            except IntegrityError:
                l.info('Item is already in the DB')
                return
