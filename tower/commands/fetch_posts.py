import datetime
import logging

import click

from tower.database import Session
from tower.model import Post
from tower.tumblr_client import tumblr_client


l = logging.getLogger(__name__)


@click.command('fetch-posts')
@click.argument('blog-name')
def fetch_posts(blog_name: str):
	session = Session()

	while True:
		offset = session.query(Post).filter(Post.blog_name == blog_name).count()

		l.info('Fetching "%s" posts starting at %s', blog_name, offset)

		response = tumblr_client.posts(
			'{}.tumblr.com'.format(blog_name),
			reblog_info=True,
			offset=offset
		)

		assert(len(response['posts']) > 0)

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

		session.commit()
